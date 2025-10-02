from app.extensions import db
from app.models import User
from app.models import Order
from sqlalchemy.exc import SQLAlchemyError

class OrderService:
    @staticmethod
    def create_order(buyer_id, paintings_subtotal, delivery_cost=0, status="pending"):
        # Check if buyer exists
        buyer = User.query.get(buyer_id)
        if not buyer:
            raise ValueError("Buyer does not exist")
        
        if buyer.role.lower() != "buyer":
            raise ValueError("User is not a buyer")
        try:
            total_price = float(paintings_subtotal) + float(delivery_cost)
            order = Order(
                buyer_id=buyer_id,
                paintings_subtotal=paintings_subtotal,
                delivery_cost=delivery_cost,
                total_price=total_price,
                status=status
            )
            db.session.add(order)
            db.session.commit()
            return order
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_orders():
        return Order.query.order_by(Order.created_at.desc()).all()

    @staticmethod
    def get_order_by_id(order_id):
        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Order not found")
        return order

    @staticmethod
    def update_order(order, data):
        try:
            for key, value in data.items():
                if hasattr(order, key):
                    setattr(order, key, value)

            # Recalculate total_price if costs updated
            order.total_price = float(order.paintings_subtotal) + float(order.delivery_cost)
            db.session.commit()
            return order
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_order(order):
        try:
            db.session.delete(order)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
