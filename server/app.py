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


# Initialize database with Flask app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Returns a list of all episodes
@app.route("/episodes", methods=["GET"])
def get_episodes():
    # Query all episodes from the database
    episodes = Episode.query.all()
    return jsonify([
        episode.to_dict(only=("id", "date", "number"))
        for episode in episodes
    ]), 200

# GET /episodes/<int:id> 
# Returns a single episode with its appearances and guests
@app.route("/episodes/<int:id>", methods=["GET"])
def get_episode_by_id(id):
    # Find episode by ID
    episode = Episode.query.get(id)
    # Return error if episode does not exist
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    # serialize to avoid recursion issues
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
# Returns a list of all guests
@app.route("/guests", methods=["GET"])
def get_guests():
    guests = Guest.query.all()
    # Serialize guests and return JSON
    return jsonify([
        guest.to_dict(only=("id", "name", "occupation"))
        for guest in guests
    ]), 200

# POST /appearances
# Create new appearance
@app.route("/appearances", methods=["POST"])
def create_appearance():
    data = request.get_json()

    # Ensure request contains JSON
    if not data:
        return jsonify({"errors": ["No JSON data received"]}), 400
    # Required fields for appearance creation
    required_keys = ["rating", "episode_id", "guest_id"]
    for key in required_keys:
        if key not in data:
            return jsonify({"errors": [f"Missing field: {key}"]}), 400

    try:
        # Create new Appearance object
        appearance = Appearance(
            rating=int(data["rating"]),
            episode_id=int(data["episode_id"]),
            guest_id=int(data["guest_id"])
        )

        # Add and commit to database
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

    # Handle invalid input values
    except ValueError as ve:
        db.session.rollback()
        return jsonify({"errors": [str(ve)]}), 422
    # Catch other errors
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500
