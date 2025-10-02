from flask import request, jsonify
from app.services.review_service import ReviewService
from app.models.review import Review


class ReviewController:
    @staticmethod
    def add_review():
        data = request.get_json()
        try:
            review = ReviewService.add_review(
                painting_id=data.get("painting_id"),
                user_id=data.get("user_id"),
                rating=data.get("rating"),
                comment=data.get("comment")
            )
            return jsonify({
                "id": review.id,
                "painting_id": review.painting_id,
                "user_id": review.user_id,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_reviews(painting_id):
        reviews = ReviewService.get_reviews_for_painting(painting_id)
        return jsonify([
            {
                "id": r.id,
                "painting_id": r.painting_id,
                "user_id": r.user_id,
                "rating": r.rating,
                "comment": r.comment,
                "created_at": r.created_at
            }
            for r in reviews
        ])

    @staticmethod
    def update_review(review_id):
        data = request.get_json()
        try:
            review = ReviewService.get_review_by_id(review_id)
            updated = ReviewService.update_review(review, data)
            return jsonify({
                "id": updated.id,
                "painting_id": updated.painting_id,
                "user_id": updated.user_id,
                "rating": updated.rating,
                "comment": updated.comment,
                "created_at": updated.created_at
            })
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_review(review_id):
        try:
            review = ReviewService.get_review_by_id(review_id)
            ReviewService.delete_review(review)
            return jsonify({"message": "Review deleted successfully"})
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
