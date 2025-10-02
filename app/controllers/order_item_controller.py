from flask import jsonify, request
from app.services.order_item_service import OrderItemService
from app.models.order_item import OrderItem

class OrderItemController:
    @staticmethod
    def add_item():
        data = request.get_json()
        required_fields = ["order_id", "painting_id", "quantity"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        try:
            item = OrderItemService.add_item(
                order_id=data["order_id"],
                painting_id=data["painting_id"],
                quantity=data.get("quantity", 1)
            )
            return jsonify({
                "id": item.id,
                "order_id": item.order_id,
                "painting_id": item.painting_id,
                "price": str(item.price),
                "quantity": item.quantity
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            import traceback; traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500

    @staticmethod
    def get_items(order_id):
        items = OrderItemService.get_items_by_order(order_id)
        return jsonify([
            {
                "id": i.id,
                "order_id": i.order_id,
                "painting_id": i.painting_id,
                "price": str(i.price),
                "quantity": i.quantity
            } for i in items
        ])

    @staticmethod
    def update_item(item_id):
        data = request.get_json()
        item = OrderItem.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        try:
            updated = OrderItemService.update_item(item, data)
            return jsonify({
                "id": updated.id,
                "order_id": updated.order_id,
                "painting_id": updated.painting_id,
                "price": str(updated.price),
                "quantity": updated.quantity
            })
        except Exception as e:
            import traceback; traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500

    @staticmethod
    def delete_item(item_id):
        item = OrderItem.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        try:
            OrderItemService.delete_item(item)
            return jsonify({"message": "Item deleted successfully"})
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred."}), 500
