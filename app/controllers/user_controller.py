from flask import request, jsonify
from app.services.user_service import UserService

class UserController:
    @staticmethod
    def register():
        data = request.get_json()
        required_fields = ["username", "email", "password"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        try:
            user = UserService.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                role=data.get("role", "buyer")
            )
            return jsonify({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        # except Exception as e:
        #     return jsonify({"error": "Unexpected error occurred"}), 500
        except Exception as e:
            import traceback
            print("REGISTER ERROR:", str(e))
            print(traceback.format_exc())
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def login():
        data = request.get_json()
        required_fields = ["email", "password"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        try:
            user = UserService.authenticate_user(
                email=data["email"],
                password=data["password"]
            )
            return jsonify({
                "message": f"Welcome back, {user.username}!"
        }), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Unexpected error occurred"}), 500

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Unexpected error occurred"}), 500

    @staticmethod
    def get_user(user_id):
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        })
    
    @staticmethod
    def get_all_users():
        users = UserService.get_all_users()
        return jsonify([
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            } for user in users
        ])
