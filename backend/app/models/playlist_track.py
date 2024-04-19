from app.extensions import db 

class PlaylistTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id', ondelete='CASCADE'))
    track_id = db.Column(db.Integer, db.ForeignKey('track.id', ondelete='CASCADE'))
