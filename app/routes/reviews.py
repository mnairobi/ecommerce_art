from flask import Blueprint
from app.controllers.review_controller import ReviewController

review_bp = Blueprint("reviews", __name__)

review_bp.route("/", methods=["POST"])(ReviewController.add_review)
review_bp.route("/painting/<int:painting_id>", methods=["GET"])(ReviewController.get_reviews)
review_bp.route("/<int:review_id>", methods=["PUT"])(ReviewController.update_review)
review_bp.route("/<int:review_id>", methods=["DELETE"])(ReviewController.delete_review)
