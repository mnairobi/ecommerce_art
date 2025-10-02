from app.models.artist import Artist
from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError

class ArtistService:
    @staticmethod
    def create_artist(user_id, bio, social_links=None):
        if not User.query.get(user_id):
            raise ValueError("User does not exist")
        if Artist.query.filter_by(user_id=user_id).first():
            raise ValueError("Artist profile already exists for this user")

        artist = Artist(user_id=user_id, bio=bio, social_links=social_links)
        db.session.add(artist)
        try:
            db.session.commit()
            return artist
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def update_artist(artist_id, user_id, data):
        artist = Artist.query.get(artist_id)
        if not artist:
            raise ValueError("Artist not found")
        if artist.user_id != user_id:
            raise ValueError("You can only update your own artist profile")
        for key, value in data.items():
            if hasattr(artist, key):
                setattr(artist, key, value)
        try:
            db.session.commit()
            return artist
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def delete_artist(artist_id, user_id):
        artist = Artist.query.get(artist_id)
        if not artist:
            raise ValueError("Artist not found")

        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        if user.role != "admin" and artist.user_id != user_id:
            raise ValueError("You can only delete your own artist profile")

        try:
            db.session.delete(artist)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def delete_all_artists(user_id):
        """
        Admin-only: delete all artist profiles.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        if user.role != "admin":
            raise ValueError("Only admins can delete all artist profiles")

        try:
            num_deleted = Artist.query.delete()
            db.session.commit()
            return num_deleted
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def get_artist_by_user(user_id):
        return Artist.query.filter_by(user_id=user_id).first()

    @staticmethod
    def list_artists():
        return Artist.query.all()
