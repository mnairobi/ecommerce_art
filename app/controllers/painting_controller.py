from flask import jsonify, request
from app.services.painting_service import PaintingService

class PaintingController:
    @staticmethod
    def create_painting():
        data = request.get_json()
        required_fields = ["artist_id", "title", "price", "image_url"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        try:
            painting = PaintingService.create_painting(
                artist_id=data["artist_id"],
                title=data["title"],
                description=data.get("description"),
                price=data["price"],
                image_url=data["image_url"]
            )
            return jsonify({
                "id": painting.id,
                "title": painting.title,
                "description": painting.description,
                "artist_id": painting.artist_id,
                "price": str(painting.price),
                "image_url": painting.image_url
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()  # <-- this prints the full error in your console
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def get_all_paintings():
        paintings = PaintingService.get_all_paintings()
        return jsonify([
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "artist_id": p.artist_id,
                "price": str(p.price),
                "image_url": p.image_url
            } for p in paintings
        ])

    @staticmethod
    def get_painting_by_id(painting_id):
        try:
            painting = PaintingService.get_painting_by_id(painting_id)
            return jsonify({
                "id": painting.id,
                "title": painting.title,
                "description": painting.description,
                "artist_id": painting.artist_id,
                "price": str(painting.price),
                "image_url": painting.image_url
            })
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred."}), 500

    @staticmethod
    def update_painting(painting_id):
        try:
            data = request.get_json()
            painting = PaintingService.get_painting_by_id(painting_id)
            updated = PaintingService.update_painting(painting, data)
            return jsonify({
                "id": updated.id,
                "title": updated.title,
                "description": updated.description,
                "artist_id": updated.artist_id,
                "price": str(updated.price),
                "image_url": updated.image_url
            })
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
      
        except Exception as e:
            import traceback
            traceback.print_exc()  # prints the full error in the console
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def delete_painting(painting_id):
        try:
            painting = PaintingService.get_painting_by_id(painting_id)
            PaintingService.delete_painting(painting)
            return jsonify({"message": "Painting deleted successfully"})
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred."}), 500