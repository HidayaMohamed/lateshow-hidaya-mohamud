from app import app
from models import db, Episode, Guest, Appearance

with app.app_context():
    db.drop_all()
    db.create_all()

    e1 = Episode(date="1/11/99", number=1)
    e2 = Episode(date="1/12/99", number=2)

    g1 = Guest(name="Michael J. Fox", occupation="actor")
    g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
    g3 = Guest(name="Tracey Ullman", occupation="television actress")

    a1 = Appearance(rating=4, episode=e1, guest=g1)
    a2 = Appearance(rating=5, episode=e2, guest=g3)

    db.session.add_all([e1, e2, g1, g2, g3, a1, a2])
    db.session.commit()
