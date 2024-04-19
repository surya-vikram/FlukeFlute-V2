from app.extensions import db 

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    tracks = db.relationship('Track', backref='genre')
