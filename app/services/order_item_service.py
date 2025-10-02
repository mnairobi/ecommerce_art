from app.extensions import db
from app.models.order_item import OrderItem
from app.models.order import Order
from app.models.painting import Painting
from sqlalchemy.exc import SQLAlchemyError

class OrderItemService:
    @staticmethod
    def add_item(order_id, painting_id,quantity=1):
        try:
            # ✅ Validate order exists
            order = Order.query.get(order_id)
            if not order:
                raise ValueError("Order does not exist.")

            # ✅ Validate painting exists
            painting = Painting.query.get(painting_id)
            if not painting:
                raise ValueError("Painting does not exist.")

            # ✅ Create order item
            item = OrderItem(
                order_id=order_id,
                painting_id=painting_id,
                price=painting.price,
                quantity=quantity
            )
            db.session.add(item)
            db.session.commit()
            return item
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_items_by_order(order_id):
        return OrderItem.query.filter_by(order_id=order_id).all()

    @staticmethod
    def update_item(item, data):
        try:
         
            if "quantity" in data:
                item.quantity = data["quantity"]
            # Optionally, always sync price with painting
            painting = Painting.query.get(item.painting_id)
            if painting:
                item.price = painting.price
            db.session.commit()
            return item
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_item(item):
        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
