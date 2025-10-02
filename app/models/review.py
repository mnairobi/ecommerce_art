from app.extensions import db

from datetime import datetime

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    painting_id = db.Column(db.Integer, db.ForeignKey("paintings.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("rating BETWEEN 1 AND 5", name="rating_check"),
    )
