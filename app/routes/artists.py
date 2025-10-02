from flask import Blueprint
from app.controllers.artist_controller import ArtistController

artist_bp = Blueprint("artists", __name__)

# Create an artist
artist_bp.route("/", methods=["POST"])(ArtistController.create_artist)

# Update an artist
artist_bp.route("/<int:artist_id>", methods=["PUT"])(ArtistController.update_artist)

# Delete an artist
artist_bp.route("/<int:artist_id>", methods=["DELETE"])(ArtistController.delete_artist)

# Delete all artists (admin only)
artist_bp.route("/all", methods=["DELETE"])(ArtistController.delete_all_artists)

# Get artist by user_id
artist_bp.route("/user/<int:user_id>", methods=["GET"])(ArtistController.get_artist_by_user)

# List all artists
artist_bp.route("/", methods=["GET"])(ArtistController.list_artists)
