from flask import Blueprint
from app.controllers.order_item_controller import OrderItemController

order_item_bp = Blueprint("orderItems", __name__)

order_item_bp.route("/", methods=["POST"])(OrderItemController.add_item)
order_item_bp.route("/order/<int:order_id>", methods=["GET"])(OrderItemController.get_items)
order_item_bp.route("/<int:item_id>", methods=["PUT"])(OrderItemController.update_item)
order_item_bp.route("/<int:item_id>", methods=["DELETE"])(OrderItemController.delete_item)
