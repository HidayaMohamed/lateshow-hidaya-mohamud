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

    # Includes appearances
    # Each appearance includes nested guest
    return jsonify(
        episode.to_dict(
            include={"appearances": {"include": {"guest"}}}
        )
    ), 200


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

    try:
        appearance = Appearance(
            rating=data["rating"],
            episode_id=data["episode_id"],
            guest_id=data["guest_id"]
        )

        db.session.add(appearance)
        db.session.commit()

        return jsonify(
            appearance.to_dict(
                include=("episode", "guest")
            )
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 422
