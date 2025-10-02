from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db

from sqlalchemy.exc import IntegrityError

class UserService:
    @staticmethod
    def create_user(username, email, password, role="buyer"):
        hashed_pw = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_pw, role=role)
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Username or email already exists")

    @staticmethod
    def authenticate_user(email, password):
        if not email or not password:
            raise ValueError("Email and password are required")
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("User not found")
        if not check_password_hash(user.password, password):
            raise ValueError("Invalid password")
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_all_users():
        return User.query.all()