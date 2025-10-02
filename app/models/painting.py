from app.extensions import db

from datetime import datetime

class Painting(db.Model):
    __tablename__ = "paintings"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist_profiles.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default="available")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = db.relationship("OrderItem", backref="painting", cascade="all, delete-orphan")
    reviews = db.relationship("Review", backref="painting", cascade="all, delete-orphan")
