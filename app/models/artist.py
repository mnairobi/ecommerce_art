from app.extensions import db

class Artist(db.Model):
    __tablename__ = "artist_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))
    social_links = db.Column(db.JSON)

    paintings = db.relationship("Painting", backref="artist", cascade="all, delete-orphan")
