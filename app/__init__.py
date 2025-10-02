from flask import Flask
from app.routes.paintings import painting_bp
from app.routes.orders import order_bp
from app.routes.users import user_bp
from app.routes.artists import artist_bp    # ✅ import artist routes
from app.routes.order_items import order_item_bp  
from app.routes.reviews import review_bp  # ✅ import review routes
from app.routes.payments import payment_bp
from app.extensions import db, migrate  # ✅ import from extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.debug = True 

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    app.register_blueprint(painting_bp, url_prefix="/paintings")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(artist_bp, url_prefix="/artists") 
    app.register_blueprint(order_bp, url_prefix="/orders")
    app.register_blueprint(order_item_bp, url_prefix="/orderItems")
    app.register_blueprint(review_bp, url_prefix="/reviews")  # ✅ register review routes
    app.register_blueprint(payment_bp, url_prefix="/payments")

    return app

