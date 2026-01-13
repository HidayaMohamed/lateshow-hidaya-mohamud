#   Imports
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance
from flask_cors import CORS



# App instance
app = Flask(__name__)

CORS(app)
# Configured the database and stop tracking notification
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
migrate = Migrate(app, db)

# GET /episodes
@app.route("/episodes", methods=["GET"])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([
        episode.to_dict(only=("id", "date", "number"))
        for episode in episodes
    ]), 200

# GET /episodes/<int:id> -> GET episodes by id
@app.route("/episodes/<int:id>", methods=["GET"])
def get_episode_by_id(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    # Safely serialize appearances and their guests
    return jsonify({
        "id": episode.id,
        "date": episode.date,
        "number": episode.number,
        "appearances": [
            {
                "id": app.id,
                "rating": app.rating,
                "guest": {
                    "id": app.guest.id,
                    "name": app.guest.name,
                    "occupation": app.guest.occupation
                }
            } for app in episode.appearances
        ]
    }), 200

# GET /guests
@app.route("/guests", methods=["GET"])
def get_guests():
    guests = Guest.query.all()
    return jsonify([
        guest.to_dict(only=("id", "name", "occupation"))
        for guest in guests
    ]), 200

# POST /appearances
@app.route("/appearances", methods=["POST"])
def create_appearance():
    data = request.get_json()

    if not data:
        return jsonify({"errors": ["No JSON data received"]}), 400

    required_keys = ["rating", "episode_id", "guest_id"]
    for key in required_keys:
        if key not in data:
            return jsonify({"errors": [f"Missing field: {key}"]}), 400

    try:
        appearance = Appearance(
            rating=int(data["rating"]),
            episode_id=int(data["episode_id"]),
            guest_id=int(data["guest_id"])
        )

        db.session.add(appearance)
        db.session.commit()

        # Return the episode with appearances updated
        episode = Episode.query.get(appearance.episode_id)
        return jsonify({
            "id": episode.id,
            "date": episode.date,
            "number": episode.number,
            "appearances": [
                {
                    "id": app.id,
                    "rating": app.rating,
                    "guest": {
                        "id": app.guest.id,
                        "name": app.guest.name,
                        "occupation": app.guest.occupation
                    }
                } for app in episode.appearances
            ]
        }), 201

    except ValueError as ve:
        db.session.rollback()
        return jsonify({"errors": [str(ve)]}), 422

    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500
