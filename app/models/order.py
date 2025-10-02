from app.extensions import db

from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    paintings_subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_cost = db.Column(db.Numeric(10, 2), default=0)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")
    payment = db.relationship("Payment", backref="order", uselist=False, cascade="all, delete-orphan")
    delivery = db.relationship("Delivery", backref="order", uselist=False, cascade="all, delete-orphan")
