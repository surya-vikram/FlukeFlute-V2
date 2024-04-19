from app.extensions import db 
from app.models import Rating
from datetime import datetime
from sqlalchemy import func

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    lyrics = db.Column(db.Text)
    audio_path = db.Column(db.String, nullable=False)
    playback_count = db.Column(db.Integer, default=0)
    release_date = db.Column(db.Date, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id', ondelete='CASCADE'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id', ondelete='CASCADE'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id', ondelete='CASCADE'))
    ratings = db.relationship('User', secondary='rating')

    def increment_playback(self):
        self.playback_count += 1
        db.session.commit()

    @staticmethod
    def trending(limit=10):
        return Track.query.order_by(Track.playback_count.desc()).limit(limit).all()

    def avg_rating(self):
        ratings = [rating.rating_value for rating in Rating.query.filter_by(track_id=self.id).all()]
        return round(sum(ratings) / len(ratings), 1) if ratings else 'Unrated'

    @staticmethod
    def top_rated(limit=10):
        return (db.session.query(Track)
                .join(Rating, Rating.track_id == Track.id)
                .group_by(Track.id)
                .order_by(func.avg(Rating.rating_value).desc())
                .limit(limit)
                .all())

