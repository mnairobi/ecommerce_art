from flask import Blueprint
from app.controllers.user_controller import UserController

user_bp = Blueprint("users", __name__)

user_bp.route("/register", methods=["POST"])(UserController.register)
user_bp.route("/login", methods=["POST"])(UserController.login)
user_bp.route("/<int:user_id>", methods=["GET"])(UserController.get_user)
user_bp.route("/", methods=["GET"])(UserController.get_all_users)