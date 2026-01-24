from __future__ import annotations
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Użytkownik aplikacji (logowanie, profil)."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(190), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Product(db.Model):
    """Produkt oszczędnościowy dodawany ręcznie przez użytkownika."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    unit = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    updated_at = db.Column(db.Date, nullable=False, default=date.today)
    __table_args__ = (db.UniqueConstraint("user_id", "name", "unit", name="uq_prod"),)

class SavingsDay(db.Model):
    """Zbiorcze oszczędności użytkownika dla jednego dnia."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    day = db.Column(db.Date, nullable=False, default=date.today)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    __table_args__ = (db.UniqueConstraint("user_id", "day", name="uq_sday"),)

class SavingsItem(db.Model):
    """Pojedyncza pozycja oszczędności (produkt, ilość, cena)."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    day = db.Column(db.Date, nullable=False, default=date.today)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    unit = db.Column(db.String(30), nullable=False)
    qty = db.Column(db.Numeric(12, 3), nullable=False, default=0)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)

class Allocation(db.Model):
    """Procentowy podział inwestycji użytkownika na instrumenty."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    instrument = db.Column(db.String(120), nullable=False)
    percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    __table_args__ = (db.UniqueConstraint("user_id", "instrument", name="uq_alloc"),)

class Batch(db.Model):
    """Jedno zbiorcze zainwestowanie oszczędności z danego dnia."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    savings_day = db.Column(db.Date, nullable=False)
    executed_day = db.Column(db.Date, nullable=False, default=date.today)
    executed_hhmm = db.Column(db.String(5), nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    __table_args__ = (db.UniqueConstraint("user_id", "savings_day", name="uq_batch"),)

class Lot(db.Model):
    """Pojedyncza pozycja inwestycyjna (instrument, cena, ilość)."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey("batch.id"), nullable=False)
    created_at = db.Column(db.Date, nullable=False, default=date.today)
    instrument = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    price = db.Column(db.Numeric(18, 6), nullable=False, default=0)
    units = db.Column(db.Numeric(24, 10), nullable=False, default=0)

class Quote(db.Model):
    """Notowanie instrumentu w danym dniu i godzinie."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    day = db.Column(db.Date, nullable=False, default=date.today)
    hhmm = db.Column(db.String(5), nullable=False)
    instrument = db.Column(db.String(120), nullable=False)
    value = db.Column(db.Numeric(18, 6), nullable=False, default=0)
    __table_args__ = (db.UniqueConstraint("user_id", "day", "hhmm", "instrument", name="uq_quote"),)
