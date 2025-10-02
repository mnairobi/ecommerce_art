from app.extensions import db
from app.models.review import Review
from app.models.painting import Painting
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError


class ReviewService:
    @staticmethod
    def add_review(painting_id, user_id, rating, comment):
        try:
            # ✅ Validate painting exists
            painting = Painting.query.get(painting_id)
            if not painting:
                raise ValueError("Painting not found.")

            # ✅ Validate user exists
            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found.")
            if user.role.lower() != "buyer":
                raise ValueError("Only buyers can add reviews.")
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")
            
            # ✅ Check duplicate (user can review a painting only once)
            existing_review = Review.query.filter_by(
                painting_id=painting_id, user_id=user_id
            ).first()
            if existing_review:
                raise ValueError("You already reviewed this painting.")

            review = Review(
                painting_id=painting_id,
                user_id=user_id,
                rating=rating,
                comment=comment
            )
            db.session.add(review)
            db.session.commit()
            return review
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_reviews_for_painting(painting_id):
        return Review.query.filter_by(painting_id=painting_id).order_by(Review.created_at.desc()).all()

    @staticmethod
    def get_review_by_id(review_id):
        review = Review.query.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        return review

    @staticmethod
    def update_review(review, data):
        try:
            if "rating" in data:
                if not (1 <= data["rating"] <= 5):
                    raise ValueError("Rating must be between 1 and 5.")
                review.rating = data["rating"]

            if "comment" in data:
                review.comment = data["comment"]

            db.session.commit()
            return review
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_review(review):
        try:
            db.session.delete(review)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
