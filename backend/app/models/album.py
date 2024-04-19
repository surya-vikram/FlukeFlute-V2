from app.extensions import db 
from datetime import datetime

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cover_path = db.Column(db.String, default="album.jpg")
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    tracks = db.relationship('Track', backref='album')


