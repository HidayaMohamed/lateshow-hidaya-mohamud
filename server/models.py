# imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Episode(db.Model, SerializerMixin):
    __tablename__ = "episodes"

    # Serialization to prevent recursion 
    serialize_rules = ("-appearances.episode","-guests.appearances")

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    # Relationships
    appearances = db.relationship(
        "Appearance",
        back_populates="episode",
        cascade="all, delete-orphan"
    )

    guests = db.relationship(
        "Guest",
        secondary="appearances",
        viewonly=True
    )

class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"

    # Serialization
    serialize_rules = ("-appearances.guest","-episodes.appearances")

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    # Relationships
    appearances = db.relationship(
        "Appearance",
        back_populates="guest",
        cascade="all, delete-orphan"
    )

    episodes = db.relationship(
        "Episode",
        secondary="appearances",
        viewonly=True
    )


class Appearance(db.Model, SerializerMixin):
    __tablename__ = "appearances"

    serialize_rules = (
        "-episode.appearances",
        "-guest.appearances",
    )

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

    # Relationship
    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    # Validation for rating to be between 1 and 5 
    @validates("rating")
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return value 
