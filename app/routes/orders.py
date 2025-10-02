from flask import Blueprint
from app.controllers.order_controller import OrderController

order_bp = Blueprint("orders", __name__)

order_bp.add_url_rule("/", view_func=OrderController.create_order, methods=["POST"])
order_bp.add_url_rule("/", view_func=OrderController.get_all_orders, methods=["GET"])
order_bp.add_url_rule("/<int:order_id>", view_func=OrderController.get_order_by_id, methods=["GET"])
order_bp.add_url_rule("/<int:order_id>", view_func=OrderController.update_order, methods=["PUT"])
order_bp.add_url_rule("/<int:order_id>", view_func=OrderController.delete_order, methods=["DELETE"])
