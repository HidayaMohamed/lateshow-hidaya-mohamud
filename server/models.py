# imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Episode(db.Model, SerializerMixin):
    __tablename__ = "episodes"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)


class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)


class Appearance(db.Model, SerializerMixin):
    __tablename__ = "appearances"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    # Foreign keys
    episode_id = db.Column(
        db.Integer,
        db.ForeignKey("episodes.id", ondelete="CASCADE"),
        nullable=False
    )
    guest_id = db.Column(
        db.Integer,
        db.ForeignKey("guests.id", ondelete="CASCADE"),
        nullable=False
    )