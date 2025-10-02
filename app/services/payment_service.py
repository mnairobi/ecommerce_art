from app.extensions import db
from app.models.payment import Payment
from app.models.order import Order
from sqlalchemy.exc import SQLAlchemyError


class PaymentService:
    @staticmethod
    def create_payment(order_id, transaction_id, phone_number, amount):
        try:
            # ✅ Validate order exists
            order = Order.query.get(order_id)
            if not order:
                raise ValueError("Order not found.")

            # ✅ Ensure order total matches payment amount
            if float(order.total_price) != float(amount):
                raise ValueError("Payment amount does not match order total.")

            # ✅ Prevent duplicate transaction IDs
            existing_payment = Payment.query.filter_by(transaction_id=transaction_id).first()
            if existing_payment:
                raise ValueError("Transaction ID already exists.")

            payment = Payment(
                order_id=order_id,
                transaction_id=transaction_id,
                phone_number=phone_number,
                amount=amount,
                status="initiated"
            )
            db.session.add(payment)

            # Optionally: mark order as 'processing'
            order.status = "processing"

            db.session.commit()
            return payment
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_payment(payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            raise ValueError("Payment not found.")
        return payment

    @staticmethod
    def update_payment_status(payment, status):
        try:
            payment.status = status

            # Optionally: sync with order
            if status == "completed":
                payment.order.status = "paid"
            elif status == "failed":
                payment.order.status = "payment_failed"

            db.session.commit()
            return payment
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_payment(payment):
        try:
            db.session.delete(payment)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_payment_by_transaction_id(transaction_id):
        return Payment.query.filter_by(transaction_id=transaction_id).first()
