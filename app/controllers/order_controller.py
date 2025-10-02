from flask import jsonify, request
from app.services.order_service import OrderService

class OrderController:
    @staticmethod
    def create_order():
        data = request.get_json()
        required_fields = ["buyer_id", "paintings_subtotal"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        try:
            order = OrderService.create_order(
                buyer_id=data["buyer_id"],
                paintings_subtotal=data["paintings_subtotal"],
                delivery_cost=data.get("delivery_cost", 0),
                status=data.get("status", "pending")
            )
            return jsonify(OrderController.serialize(order)), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_all_orders():
        orders = OrderService.get_all_orders()
        return jsonify([OrderController.serialize(o) for o in orders])

    @staticmethod
    def get_order_by_id(order_id):
        try:
            order = OrderService.get_order_by_id(order_id)
            return jsonify(OrderController.serialize(order))
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception:
            return jsonify({"error": "Unexpected error occurred"}), 500

    @staticmethod
    def update_order(order_id):
        try:
            data = request.get_json()
            order = OrderService.get_order_by_id(order_id)
            updated = OrderService.update_order(order, data)
            return jsonify(OrderController.serialize(updated))
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_order(order_id):
        try:
            order = OrderService.get_order_by_id(order_id)
            OrderService.delete_order(order)
            return jsonify({"message": "Order deleted successfully"})
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception:
            return jsonify({"error": "Unexpected error occurred"}), 500

    @staticmethod
    def serialize(order):
        return {
            "id": order.id,
            "buyer_id": order.buyer_id,
            "paintings_subtotal": str(order.paintings_subtotal),
            "delivery_cost": str(order.delivery_cost),
            "total_price": str(order.total_price),
            "status": order.status,
            "created_at": order.created_at.isoformat()
        }
