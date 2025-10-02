from app.extensions import db

from datetime import datetime

class Delivery(db.Model):
    __tablename__ = "deliveries"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    delivery_status = db.Column(db.String(20), default="pending")
    delivery_cost = db.Column(db.Numeric(10, 2), nullable=False)
    courier_name = db.Column(db.String(100))
    delivery_date = db.Column(db.DateTime, default=datetime.utcnow)
