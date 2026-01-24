from __future__ import annotations

import time
import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Optional, Tuple

import requests
from bs4 import BeautifulSoup

# URL-e źródeł notowań Bankiera
URL_FOREX_TABLE = "https://www.bankier.pl/waluty/kursy-walut/forex/EURCHF"
URL_COMMODITIES = "https://www.bankier.pl/surowce/notowania"

# Cache wyników (TTL)
TTL_SECONDS = 60
_CACHE: dict = {"ts": 0.0, "data": None}

# Obsługiwane pary walutowe
FX_KEYS = ["EUR/PLN", "USD/PLN", "CHF/PLN"]

# Obsługiwane surowce
COM_KEYS = ["ZŁOTO", "MIEDŹ", "ROPA"]

# Możliwe etykiety surowców na stronie
COM_LABELS = {
    "ZŁOTO": ["Złoto", "ZŁOTO"],
    "MIEDŹ": ["Miedź", "MIEDŹ", "Miedź COMEX", "MIEDŹ COMEX"],
    "ROPA": ["Ropa", "ROPA", "ROPA WTI", "Ropa WTI", "Ropa Brent", "ROPA BRENT"],
}

# Pomocnicze skróty Decimal
D = lambda x: Decimal(str(x))
q6 = lambda x: D(x).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def _get_html(url: str) -> str:
    """Pobiera HTML strony Bankiera z poprawnymi nagłówkami."""
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        },
        timeout=20,
    )
    r.raise_for_status()
    return r.text


def _text(html: str) -> str:
    """Czyści HTML do samego tekstu (łatwiejsze parsowanie regex)."""
    return BeautifulSoup(html, "html.parser").get_text("\n", strip=True)


def _num_pl(s: str) -> Decimal:
    """Parsuje liczbę w polskim formacie (spacje, przecinki)."""
    s = (s or "").replace("\xa0", " ").strip()
    s = re.sub(r"\s+", "", s).replace(",", ".")
    return D(s)


def _pct_pl(s: str) -> Decimal:
    """Parsuje procent (np. +1,23%) do Decimal."""
    s = (s or "").strip().replace("%", "").replace(",", ".")
    return D(s)


def _parse_fx_from_table(html: str) -> Tuple[Dict[str, Decimal], Dict[str, Decimal]]:
    """Wyciąga kursy walut i zmiany % z tabeli Forex."""
    t = _text(html)
    prices: Dict[str, Decimal] = {}
    changes: Dict[str, Decimal] = {}

    for pair in FX_KEYS:
        m = re.search(
            rf"{re.escape(pair)}\s*([0-9][0-9\s.,]*)\s*([+-]?[0-9][0-9\s.,]*)%",
            t,
        )
        if not m:
            continue
        try:
            prices[pair] = q6(_num_pl(m.group(1)))
            changes[pair] = _pct_pl(m.group(2))
        except Exception:
            pass

    return prices, changes


def _parse_commodities_usd_and_change(
    html: str,
) -> Tuple[Dict[str, Decimal], Dict[str, Decimal], Optional[str]]:
    """Wyciąga ceny surowców w USD, zmiany % oraz godzinę notowania."""
    t = _text(html)
    prices_usd: Dict[str, Decimal] = {}
    changes: Dict[str, Decimal] = {}

    # Próba znalezienia godziny notowania
    m_time = re.search(r"\b(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\b", t)
    time_hhmm = m_time.group(2) if m_time else None

    for key, labels in COM_LABELS.items():
        for lbl in labels:
            m = re.search(
                rf"{re.escape(lbl)}\s*([0-9][0-9\s.,]*)\s*([+-]?[0-9][0-9\s.,]*)%",
                t,
            )
            if not m:
                continue
            try:
                prices_usd[key] = q6(_num_pl(m.group(1)))
                changes[key] = _pct_pl(m.group(2))
                break
            except Exception:
                pass

    return prices_usd, changes, time_hhmm


def get_bankier_quotes_pln() -> dict:
    """Zwraca aktualne notowania w PLN (z cache TTL)."""
    now = time.time()
    if _CACHE["data"] and (now - _CACHE["ts"] < TTL_SECONDS):
        return _CACHE["data"]

    prices: Dict[str, Decimal] = {}
    changes: Dict[str, Decimal] = {}

    # Waluty
    try:
        fx_html = _get_html(URL_FOREX_TABLE)
        fx_prices, fx_changes = _parse_fx_from_table(fx_html)
        prices.update(fx_prices)
        changes.update(fx_changes)
    except Exception:
        pass

    # Surowce
    t_com = None
    com_usd: Dict[str, Decimal] = {}
    try:
        com_html = _get_html(URL_COMMODITIES)
        com_usd, com_changes, t_com = _parse_commodities_usd_and_change(com_html)
        changes.update(com_changes)
    except Exception:
        pass

    # Przeliczenie surowców USD → PLN
    usdpln = prices.get("USD/PLN")
    if usdpln:
        for k in COM_KEYS:
            if k in com_usd:
                prices[k] = q6(com_usd[k] * usdpln)

    data = {"prices": prices, "changes": changes, "time_hhmm": t_com}
    _CACHE["ts"] = now
    _CACHE["data"] = data
    return data
