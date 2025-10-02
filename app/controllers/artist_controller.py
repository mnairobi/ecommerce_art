from flask import jsonify, request
from app.services.artist_service import ArtistService
from app.models.user import User

class ArtistController:
    @staticmethod
    def create_artist():
        data = request.get_json()
        required_fields = ["user_id", "bio"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        user_id = data["user_id"]

        try:
            # 🔒 Check if user exists and has the correct role
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "User does not exist"}), 404

            if user.role not in ["artist", "admin"]:
                return jsonify({"error": "Only users with role 'artist' or 'admin' can create artist profiles"}), 403

            artist = ArtistService.create_artist(
                user_id=user_id,
                bio=data["bio"],
                social_links={"portfolio_url": data.get("portfolio_url")} if data.get("portfolio_url") else None
            )

            return jsonify({
                "id": artist.id,
                "user_id": artist.user_id,
                "bio": artist.bio,
                "social_links": artist.social_links
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500
        
    @staticmethod
    def update_artist(artist_id):
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        try:
            # 🔒 Check if user exists and has the correct role
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "User does not exist"}), 404

            artist = ArtistService.get_artist_by_user(user_id)
            if not artist or artist.id != artist_id:
                # Only allow if admin
                if user.role != "admin":
                    return jsonify({"error": "You can only update your own artist profile"}), 403

            if user.role not in ["artist", "admin"]:
                return jsonify({"error": "Only users with role 'artist' or 'admin' can update artist profiles"}), 403

            # ✅ Build update payload (allow partial updates)
            update_data = {}
            if "bio" in data:
                update_data["bio"] = data["bio"]

            if "portfolio_url" in data:
                update_data["social_links"] = {
                    "portfolio_url": data["portfolio_url"]
                }

            updated_artist = ArtistService.update_artist(artist_id, user_id, update_data)

            return jsonify({
                "id": updated_artist.id,
                "user_id": updated_artist.user_id,
                "bio": updated_artist.bio,
                "social_links": updated_artist.social_links
            })

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500


    @staticmethod
    def delete_artist(artist_id):
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        try:
            # 🔒 Check if user exists and has the correct role
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "User does not exist"}), 404

            artist = ArtistService.get_artist_by_user(user_id)
            if not artist or artist.id != artist_id:
                # Only allow if admin
                if user.role != "admin":
                    return jsonify({"error": "You can only delete your own artist profile"}), 403

            if user.role not in ["artist", "admin"]:
                return jsonify({"error": "Only users with role 'artist' or 'admin' can delete artist profiles"}), 403

            ArtistService.delete_artist(artist_id, user_id)
            return jsonify({"message": "Artist profile deleted successfully"})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500
    @staticmethod
    def get_artist_by_user(user_id):
        artist = ArtistService.get_artist_by_user(user_id)
        if not artist:
            return jsonify({"error": "Artist not found"}), 404
        return jsonify({
            "id": artist.id,
            "user_id": artist.user_id,
            "bio": artist.bio,
            "social_links": artist.social_links
        })

    @staticmethod
    def list_artists():
        artists = ArtistService.list_artists()
        return jsonify([
            {
                "id": a.id,
                "user_id": a.user_id,
                "bio": a.bio,
                "social_links": a.social_links
            } for a in artists
        ])
    @staticmethod
    def delete_all_artists():
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        try:
            num_deleted = ArtistService.delete_all_artists(user_id)
            return jsonify({"message": f"Deleted {num_deleted} artist profiles"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500
