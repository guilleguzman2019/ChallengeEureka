from app import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), index=True, nullable=False)
    apellido = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(64), index=True, nullable=False)
    key = db.Column(db.String(64), index=True, nullable=False)