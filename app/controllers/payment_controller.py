from flask import request, jsonify
from app.services.payment_service import PaymentService


class PaymentController:
    @staticmethod
    def create_payment():
        data = request.get_json()
        try:
            payment = PaymentService.create_payment(
                order_id=data.get("order_id"),
                transaction_id=data.get("transaction_id"),
                phone_number=data.get("phone_number"),
                amount=data.get("amount")
            )
            return jsonify({
                "id": payment.id,
                "order_id": payment.order_id,
                "transaction_id": payment.transaction_id,
                "phone_number": payment.phone_number,
                "amount": str(payment.amount),
                "status": payment.status,
                "payment_date": payment.payment_date
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_payment(payment_id):
        try:
            payment = PaymentService.get_payment(payment_id)
            return jsonify({
                "id": payment.id,
                "order_id": payment.order_id,
                "transaction_id": payment.transaction_id,
                "phone_number": payment.phone_number,
                "amount": str(payment.amount),
                "status": payment.status,
                "payment_date": payment.payment_date
            })
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_payment(payment_id):
        data = request.get_json()
        try:
            payment = PaymentService.get_payment(payment_id)
            updated = PaymentService.update_payment_status(payment, data.get("status"))
            return jsonify({
                "id": updated.id,
                "order_id": updated.order_id,
                "transaction_id": updated.transaction_id,
                "phone_number": updated.phone_number,
                "amount": str(updated.amount),
                "status": updated.status,
                "payment_date": updated.payment_date
            })
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_payment(payment_id):
        try:
            payment = PaymentService.get_payment(payment_id)
            PaymentService.delete_payment(payment)
            return jsonify({"message": "Payment deleted successfully"})
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def mpesa_callback():
        """
        Simulates Safaricom M-Pesa Daraja payment confirmation callback.
        Expected payload:
        {
            "transaction_id": ""TNN12345ABC",
            "status": "completed",
            "amount": 750.00,
            "phone_number": "+254712345678"
        }
        """
        data = request.get_json()
        try:
            transaction_id = data.get("transaction_id")
            status = data.get("status")

            # ✅ find payment by transaction_id
            payment = PaymentService.get_payment_by_transaction_id(transaction_id)
            if not payment:
                return jsonify({"error": "Payment not found"}), 404

            # ✅ confirm the amount matches (optional check)
            # if str(payment.amount) != str(data.get("amount")):
            #     return jsonify({"error": "Payment amount mismatch"}), 400

            # ✅ update payment & order status
            updated = PaymentService.update_payment_status(payment, status)

            return jsonify({
                "message": "Payment status updated via callback",
                "transaction_id": updated.transaction_id,
                "status": updated.status,
                "order_status": updated.order.status
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
