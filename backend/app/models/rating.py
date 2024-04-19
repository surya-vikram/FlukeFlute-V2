from app.extensions import db 

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('track.id', ondelete='CASCADE'), nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)
