from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Film(db.Model):
    __tablename__ = 'film'
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    rental_rate = db.Column(db.Float)
    length = db.Column(db.Integer)
