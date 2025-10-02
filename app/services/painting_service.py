from app.extensions import db
from app.models import Painting,Artist
from sqlalchemy.exc import SQLAlchemyError


class PaintingService:
    @staticmethod
    def create_painting(artist_id, title, description, price, image_url):
        #check if artist exists
        
        artist = Artist.query.get(artist_id)
        if not artist:
            raise ValueError("Artist does not exist")   
        try:
            painting = Painting(
                artist_id=artist_id,
                title=title,
                description=description,
                price=price,
                image_url=image_url
            )
            db.session.add(painting)
            db.session.commit()
            return painting
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_paintings():
        return Painting.query.order_by(Painting.created_at.desc()).all()
    
    @staticmethod
    def get_painting_by_id(painting_id):
        painting = Painting.query.get(painting_id)
        if not painting:
            raise ValueError("Painting not found")
        return painting

    @staticmethod
    def update_painting(painting, data):
        try:
            new_artist_id = data.get('artist_id', painting.artist_id)
            new_title = data.get('title', painting.title)

            # Case-insensitive duplicate check
            if (new_artist_id != painting.artist_id or new_title.lower() != painting.title.lower()):
                existing = Painting.query.filter(
                    Painting.artist_id == new_artist_id,
                    db.func.lower(Painting.title) == new_title.lower(),
                    Painting.id != painting.id
                ).first()
                if existing:
                    raise ValueError("This artist already has a painting with this title.")

            for key, value in data.items():
                if hasattr(painting, key):
                    setattr(painting, key, value)

            db.session.commit()
            return painting
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_painting(painting):
        try:
            db.session.delete(painting)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
