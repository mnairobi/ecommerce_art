from flask import Blueprint
from app.controllers.payment_controller import PaymentController

payment_bp = Blueprint("payments", __name__)

payment_bp.route("/", methods=["POST"])(PaymentController.create_payment)
payment_bp.route("/<int:payment_id>", methods=["GET"])(PaymentController.get_payment)
payment_bp.route("/<int:payment_id>", methods=["PUT"])(PaymentController.update_payment)
payment_bp.route("/<int:payment_id>", methods=["DELETE"])(PaymentController.delete_payment)

# ✅ Mpesa Callback Simulation
payment_bp.route("/callback", methods=["POST"])(PaymentController.mpesa_callback)