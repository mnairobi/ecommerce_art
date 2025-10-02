from flask import Blueprint
from app.controllers.painting_controller import PaintingController

painting_bp = Blueprint("paintings", __name__)

painting_bp.route("/", methods=["POST"])(PaintingController.create_painting)
painting_bp.route("/", methods=["GET"])(PaintingController.get_all_paintings)
painting_bp.route("/<int:painting_id>", methods=["GET"])(PaintingController.get_painting_by_id)
painting_bp.route("/<int:painting_id>", methods=["PUT"])(PaintingController.update_painting)
painting_bp.route("/<int:painting_id>", methods=["DELETE"])(PaintingController.delete_painting)
