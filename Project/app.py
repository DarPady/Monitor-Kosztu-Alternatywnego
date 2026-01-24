from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from models import db, User, Product, SavingsDay, SavingsItem, Allocation, Batch, Lot, Quote
from bankier_quotes import get_bankier_quotes_pln

D = lambda x: Decimal(str(x))
q2 = lambda x: D(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
q3 = lambda x: D(x).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
q6 = lambda x: D(x).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
q10 = lambda x: D(x).quantize(Decimal("0.0000000001"), rounding=ROUND_HALF_UP)

INSTR = ["USD/PLN", "EUR/PLN", "CHF/PLN", "ZŁOTO", "MIEDŹ", "ROPA"]
HOME_LABEL = {"ZŁOTO": "ZŁOTO (uncja)", "MIEDŹ": "MIEDŹ (tona)", "ROPA": "ROPA (baryłka)"}
DAILY_QUOTE_HHMM = "12:00"


def parse_pl(s: str) -> Decimal:
    """Parsuje liczbę w polskim formacie do Decimal."""
    s = (s or "").strip().replace(" ", "").replace(",", ".")
    return D(s)


def _d(s: str) -> date | None:
    """Bezpiecznie parsuje datę YYYY-MM-DD."""
    s = (s or "").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def _range_dates(df: date | None, dt: date | None, default_days: int = 30) -> tuple[date, date]:
    """Wylicza poprawny zakres dat (fallback na ostatnie N dni)."""
    today = date.today()
    if not df and not dt:
        return today - timedelta(days=default_days - 1), today
    if df and not dt:
        return df, today
    if dt and not df:
        return dt - timedelta(days=default_days - 1), dt
    if df and dt and df > dt:
        df, dt = dt, df
    return df or today, dt or today


def default_alloc(keys: list[str]) -> dict[str, Decimal]:
    """Tworzy równy domyślny podział procentowy (100%)."""
    n = len(keys) or 1
    base = q2(Decimal("100") / D(n))
    out = {k: base for k in keys}
    diff = q2(Decimal("100") - sum(out.values(), D(0)))
    if diff:
        out[keys[-1]] = q2(out[keys[-1]] + diff)
    return out


def get_alloc_map(user_id: int) -> dict[str, Decimal]:
    """Zwraca mapę alokacji użytkownika (fallback na domyślną)."""
    rows = Allocation.query.filter_by(user_id=user_id).all()
    if not rows:
        return default_alloc(INSTR)
    m = {r.instrument: q2(r.percent) for r in rows}
    for k in INSTR:
        m.setdefault(k, Decimal("0.00"))
    return m


def set_alloc_map(user_id: int, raw: dict[str, str]) -> tuple[bool, str]:
    """Zapisuje alokację użytkownika (walidacja 100%)."""
    vals: dict[str, Decimal] = {}
    for k in INSTR:
        s = (raw.get(k) or "").strip()
        vals[k] = q2(parse_pl(s) if s else 0)
        if vals[k] < 0:
            return False, f"Ujemna wartość dla {k}"
    if q2(sum(vals.values(), D(0))) != Decimal("100.00"):
        return False, "Suma procentów musi wynosić 100%."

    ex = {r.instrument: r for r in Allocation.query.filter_by(user_id=user_id).all()}
    for k, v in vals.items():
        if k in ex:
            ex[k].percent = v
        else:
            db.session.add(Allocation(user_id=user_id, instrument=k, percent=v))
    db.session.commit()
    return True, "Zapisano."


def upsert_quote(user_id: int, day_: date, hhmm: str, instr: str, val: Decimal):
    """Aktualizuje lub dodaje notowanie."""
    q = Quote.query.filter_by(user_id=user_id, day=day_, hhmm=hhmm, instrument=instr).first()
    if q:
        q.value = val
    else:
        db.session.add(Quote(user_id=user_id, day=day_, hhmm=hhmm, instrument=instr, value=val))


def refresh_daily_quotes(user_id: int) -> tuple[dict, dict]:
    q = get_bankier_quotes_pln()
    prices = q.get("prices", {}) or {}
    changes = q.get("changes", {}) or {}
    if prices:
        today = date.today()
        for k, v in prices.items():
            upsert_quote(user_id, today, DAILY_QUOTE_HHMM, k, q6(v))
        db.session.commit()
    return prices, changes


def add_savings(user_id: int, day_: date, prod: Product, qty: Decimal):
    qty = q3(qty)
    unit_price = q2(prod.price)
    total = q2(qty * unit_price)

    it = SavingsItem.query.filter_by(user_id=user_id, day=day_, product_id=prod.id).first()
    if it:
        it.qty = q3(D(it.qty) + qty)
        it.unit_price = unit_price
        it.total = q2(D(it.total) + total)
    else:
        db.session.add(
            SavingsItem(
                user_id=user_id,
                day=day_,
                product_id=prod.id,
                name=prod.name,
                unit=prod.unit,
                qty=qty,
                unit_price=unit_price,
                total=total,
            )
        )

    sday = SavingsDay.query.filter_by(user_id=user_id, day=day_).first()
    if not sday:
        sday = SavingsDay(user_id=user_id, day=day_, total=Decimal("0.00"))
        db.session.add(sday)
    sday.total = q2(D(sday.total) + total)
    db.session.commit()


def pending_days(user_id: int) -> list[date]:
    today = date.today()
    days = (
        SavingsDay.query.filter(SavingsDay.user_id == user_id, SavingsDay.day < today, SavingsDay.total > 0)
        .order_by(SavingsDay.day.asc())
        .all()
    )
    out: list[date] = []
    for d in days:
        if not Batch.query.filter_by(user_id=user_id, savings_day=d.day).first():
            out.append(d.day)
    return out


def invest_for_day(user_id: int, savings_day: date, enforce_time: bool) -> tuple[bool, str]:
    if enforce_time and datetime.now().hour < 16:
        return False, "Jeszcze nie pora."
    if Batch.query.filter_by(user_id=user_id, savings_day=savings_day).first():
        return False, "Już zainwestowano ten dzień."

    sd = SavingsDay.query.filter_by(user_id=user_id, day=savings_day).first()
    if not sd or D(sd.total) <= 0:
        return False, "Brak oszczędności."

    prices, _ = refresh_daily_quotes(user_id)
    if any(k not in prices for k in INSTR):
        return False, "Brak części notowań (Bankier). Spróbuj ponownie."

    total = q2(sd.total)
    hhmm = datetime.now().strftime("%H:%M")

    b = Batch(user_id=user_id, savings_day=savings_day, executed_day=date.today(), executed_hhmm=hhmm, total=total)
    db.session.add(b)
    db.session.flush()

    alloc = get_alloc_map(user_id)
    today = date.today()

    for k in INSTR:
        pct = D(alloc.get(k, 0))
        if pct <= 0:
            continue
        amt = q2(total * pct / Decimal("100"))
        if amt <= 0:
            continue

        price = q6(prices[k])
        units = q10(amt / price) if price > 0 else D(0)

        db.session.add(Lot(user_id=user_id, batch_id=b.id, created_at=today, instrument=k, amount=amt, price=price, units=units))
        upsert_quote(user_id, today, hhmm, k, price)

    db.session.commit()
    return True, "Zainwestowano."


def _build_holdings_by_day(user_id: int, start: date, end: date) -> dict[date, dict[str, Decimal]]:
    lots = Lot.query.filter(Lot.user_id == user_id, Lot.created_at <= end).order_by(Lot.created_at.asc(), Lot.id.asc()).all()
    holdings: dict[str, Decimal] = {k: D(0) for k in INSTR}
    by_day: dict[date, list[Lot]] = {}
    for lot in lots:
        by_day.setdefault(lot.created_at, []).append(lot)

    out: dict[date, dict[str, Decimal]] = {}
    d = start
    while d <= end:
        for lot in by_day.get(d, []):
            holdings[lot.instrument] = holdings.get(lot.instrument, D(0)) + D(lot.units)
        out[d] = dict(holdings)
        d += timedelta(days=1)
    return out


def _quotes_for_days(user_id: int, start: date, end: date) -> dict[str, dict[date, Decimal]]:
    qs = Quote.query.filter(Quote.user_id == user_id, Quote.day <= end).order_by(Quote.day.asc(), Quote.hhmm.asc()).all()
    raw: dict[str, dict[date, Decimal]] = {k: {} for k in INSTR}
    for q in qs:
        if q.instrument in raw:
            raw[q.instrument][q.day] = D(q.value)

    out: dict[str, dict[date, Decimal]] = {k: {} for k in INSTR}
    for instr in INSTR:
        last = None
        d = start
        while d <= end:
            if d in raw[instr]:
                last = raw[instr][d]
            if last is not None:
                out[instr][d] = last
            d += timedelta(days=1)
    return out


def portfolio_points(user_id: int, start: date, end: date) -> list[tuple[str, float]]:
    if start > end:
        start, end = end, start

    holdings_by_day = _build_holdings_by_day(user_id, start, end)
    quotes_by_day = _quotes_for_days(user_id, start, end)

    pts: list[tuple[str, float]] = []
    d = start
    while d <= end:
        total = D(0)
        h = holdings_by_day.get(d, {})
        for instr in INSTR:
            units = h.get(instr, D(0))
            price = quotes_by_day.get(instr, {}).get(d)
            if units and price:
                total += units * price
        pts.append((d.isoformat(), float(q2(total))))
        d += timedelta(days=1)
    return pts


def svg_line(vals: list[tuple[str, float]]) -> str:
    if len(vals) < 2:
        return ""

    w, h = 980, 340
    pad_l, pad_r, pad_t, pad_b = 70, 26, 22, 66

    ys = [v for _, v in vals]
    mn, mx = min(ys), max(ys)
    if mx == mn:
        mx = mn + 1.0
    rng = mx - mn

    def X(i: int) -> float:
        return pad_l + i * (w - pad_l - pad_r) / (len(vals) - 1)

    def Y(v: float) -> float:
        return pad_t + (h - pad_t - pad_b) * (1 - (v - mn) / rng)

    pts = [(X(i), Y(v)) for i, (_, v) in enumerate(vals)]
    dpath = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)

    def nice_ticks(a: float, b: float, n: int = 4) -> list[float]:
        if b <= a:
            return [a]
        step = (b - a) / n
        return [a + step * i for i in range(n + 1)]

    x0y = h - pad_b
    elems = [
        f'<line x1="{pad_l}" y1="{x0y}" x2="{w-pad_r}" y2="{x0y}" stroke="rgba(255,255,255,0.25)"/>',
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{x0y}" stroke="rgba(255,255,255,0.25)"/>',
    ]

    for tv in nice_ticks(mn, mx, 4):
        y = Y(tv)
        elems.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{w-pad_r}" y2="{y:.1f}" stroke="rgba(255,255,255,0.08)"/>')
        elems.append(f'<text x="{pad_l-10}" y="{y+4:.1f}" text-anchor="end" font-size="12" fill="rgba(255,255,255,0.75)">{tv:.0f}</text>')

    n = len(vals)
    tick_count = 5 if n >= 5 else n
    idxs = [round(i * (n - 1) / (tick_count - 1)) for i in range(tick_count)] if tick_count > 1 else [0]
    idxs = sorted(set(idxs))

    for i in idxs:
        x = X(i)
        lab = vals[i][0]
        elems.append(f'<line x1="{x:.1f}" y1="{x0y}" x2="{x:.1f}" y2="{x0y+6}" stroke="rgba(255,255,255,0.25)"/>')
        if i == 0:
            anchor, tx = "start", x + 2
        elif i == n - 1:
            anchor, tx = "end", x - 2
        else:
            anchor, tx = "middle", x
        elems.append(f'<text x="{tx:.1f}" y="{x0y+22}" text-anchor="{anchor}" font-size="12" fill="rgba(255,255,255,0.75)">{lab}</text>')

    elems.append(f'<text x="{(pad_l + (w - pad_r))/2:.1f}" y="{h-16}" text-anchor="middle" font-size="12" fill="rgba(255,255,255,0.75)">Dzień</text>')
    elems.append(f'<text x="16" y="{(pad_t + x0y)/2:.1f}" text-anchor="middle" font-size="12" fill="rgba(255,255,255,0.75)" transform="rotate(-90 16 {(pad_t + x0y)/2:.1f})">Wartość (zł)</text>')

    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{"".join(elems)}<path d="{dpath}" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def format_quotes_table(rows: list[dict]) -> str:
    header = ["", "Nazwa", "Wartość", "Zmiana %"]
    idx_w = max(len(str(len(rows) - 1)), 1)
    name_w = max(len(header[1]), *(len(str(r.get("Nazwa", ""))) for r in rows)) if rows else len(header[1])
    val_w = max(len(header[2]), *(len(str(r.get("Wartość", ""))) for r in rows)) if rows else len(header[2])
    chg_w = max(len(header[3]), *(len(str(r.get("Zmiana", ""))) for r in rows)) if rows else len(header[3])

    def line() -> str:
        return f"+-{'-'*idx_w}-+-{'-'*name_w}-+-{'-'*val_w}-+-{'-'*chg_w}-+"

    def row(i: str, n: str, v: str, c: str) -> str:
        return f"| {i:>{idx_w}} | {n:<{name_w}} | {v:>{val_w}} | {c:>{chg_w}} |"

    out = [line(), row("", header[1], header[2], header[3]), line()]
    for i, r in enumerate(rows):
        out.append(row(str(i), str(r.get("Nazwa", "")), str(r.get("Wartość", "")), str(r.get("Zmiana", ""))))
    out.append(line())
    return "\n".join(out)


def print_quotes(rows: list[dict]):
    print(format_quotes_table(rows))


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance_simple.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
lm = LoginManager(app)
lm.login_view = "login"


@lm.user_loader
def load_user(uid: str):
    return User.query.get(int(uid))


@app.before_request
def _init():
    if not getattr(app, "_inited", False):
        with app.app_context():
            db.create_all()
        app._inited = True


@app.get("/")
def home():
    q = get_bankier_quotes_pln()
    prices = q.get("prices", {}) or {}
    changes = q.get("changes", {}) or {}

    rows = []
    for k in INSTR:
        if k not in prices:
            continue
        label = HOME_LABEL.get(k, k)
        val = f"{q2(prices[k]):.2f}".replace(".", ",")
        ch = changes.get(k)
        chs = (f"{ch:+.2f}%".replace(".", ",")) if ch is not None else ""
        rows.append({"Nazwa": label, "Wartość": val, "Zmiana": chs})

    return render_template("home.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        pw = request.form.get("password") or ""
        u = User.query.filter_by(email=email).first()
        if not u or not check_password_hash(u.password_hash, pw):
            flash("Nieprawidłowy email lub hasło.")
            return render_template("login.html")
        login_user(u)
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        pw = request.form.get("password") or ""
        if not username or not email or not pw:
            flash("Uzupełnij wszystkie pola.")
            return render_template("register.html")
        try:
            db.session.add(User(username=username, email=email, password_hash=generate_password_hash(pw)))
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Taki email lub username już istnieje.")
            return render_template("register.html")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.get("/products")
@login_required
def products():
    today = date.today()
    prods = Product.query.filter_by(user_id=current_user.id).order_by(Product.id.desc()).all()
    days = SavingsDay.query.filter_by(user_id=current_user.id).order_by(SavingsDay.day.desc()).limit(30).all()
    total_all = q2(sum(D(d.total) for d in SavingsDay.query.filter_by(user_id=current_user.id).all()))
    return render_template("products.html", products=prods, selected_day=today, today=today, savings_days=days, total_all=total_all)


@app.post("/products/add")
@login_required
def products_add():
    try:
        p = Product(user_id=current_user.id, name=(request.form.get("name") or "").strip(), unit=(request.form.get("unit") or "").strip(), price=q2(parse_pl(request.form.get("price") or "0")), updated_at=date.today())
        db.session.add(p)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Taki produkt już istnieje.")
    except Exception:
        flash("Błąd danych.")
    return redirect(url_for("products"))


@app.post("/products/<int:pid>/update")
@login_required
def products_update(pid: int):
    p = Product.query.filter_by(id=pid, user_id=current_user.id).first()
    if not p:
        flash("Brak dostępu.")
        return redirect(url_for("products"))
    try:
        p.price = q2(parse_pl(request.form.get("price") or "0"))
        p.updated_at = date.today()
        db.session.commit()
    except Exception:
        flash("Nieprawidłowa cena.")
    return redirect(url_for("products"))


@app.post("/products/<int:pid>/delete")
@login_required
def products_delete(pid: int):
    p = Product.query.filter_by(id=pid, user_id=current_user.id).first()
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect(url_for("products"))


@app.post("/products/<int:pid>/attach")
@login_required
def products_attach(pid: int):
    p = Product.query.filter_by(id=pid, user_id=current_user.id).first()
    if not p:
        flash("Brak produktu.")
        return redirect(url_for("products"))
    try:
        day_ = datetime.strptime(request.form.get("save_day") or "", "%Y-%m-%d").date()
        if day_ > date.today():
            raise ValueError
        qty = parse_pl(request.form.get("quantity") or "0")
        if qty <= 0:
            raise ValueError
    except Exception:
        flash("Nieprawidłowe dane.")
        return redirect(url_for("products"))
    add_savings(current_user.id, day_, p, qty)
    return redirect(url_for("products"))


@app.get("/dashboard")
@login_required
def dashboard():
    refresh_daily_quotes(current_user.id)

    df = _d(request.args.get("date_from") or "")
    dt = _d(request.args.get("date_to") or "")
    start, end = _range_dates(df, dt, 30)

    invest_for_day(current_user.id, date.today() - timedelta(days=1), enforce_time=True)
    refresh_daily_quotes(current_user.id)

    pts = portfolio_points(current_user.id, start, end)
    svg_port = svg_line(pts)
    last_val = pts[-1][1] if pts else 0

    lots = Lot.query.filter_by(user_id=current_user.id).order_by(Lot.id.desc()).limit(200).all()
    pend = len(pending_days(current_user.id))

    today = date.today().isoformat()
    presets = {"7": {"from": (date.today() - timedelta(days=6)).isoformat(), "to": today}, "14": {"from": (date.today() - timedelta(days=13)).isoformat(), "to": today}, "30": {"from": (date.today() - timedelta(days=29)).isoformat(), "to": today}}

    return render_template("dashboard.html", svg_value=svg_port, last_value=last_val, lots=lots, pending_count=pend, date_from=start.isoformat(), date_to=end.isoformat(), today=today, presets=presets)


@app.post("/dashboard/catchup")
@login_required
def dashboard_catchup():
    n = 0
    for day_ in pending_days(current_user.id):
        ok, _ = invest_for_day(current_user.id, day_, enforce_time=False)
        if ok:
            n += 1
    refresh_daily_quotes(current_user.id)
    flash(f"Inwestowanie: {n} dni." if n else "Brak zaległości.")
    return redirect(url_for("dashboard"))


@app.get("/profile")
@login_required
def profile():
    alloc = get_alloc_map(current_user.id)
    return render_template("profile.html", alloc_keys=INSTR, alloc_map={k: str(alloc[k]).replace(".", ",") for k in INSTR})


@app.post("/profile/allocation")
@login_required
def profile_save():
    raw = {k: (request.form.get(f"alloc_{k}") or "") for k in INSTR}
    flash(set_alloc_map(current_user.id, raw)[1])
    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(debug=True)
