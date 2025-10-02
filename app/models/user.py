from app.extensions import db

from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # hashed password
    role = db.Column(db.String(20), default="buyer")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    artist_profile = db.relationship("Artist", backref="user", uselist=False, cascade="all, delete-orphan")
    orders = db.relationship("Order", backref="buyer", cascade="all, delete-orphan")
    reviews = db.relationship("Review", backref="user", cascade="all, delete-orphan")



