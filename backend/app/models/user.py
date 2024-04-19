from app.extensions import bcrypt, db
from app.models import Role

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary='user_role', backref='users')
    stage_name = db.Column(db.String(20))
    pfp_path = db.Column(db.String(100))
    bio = db.Column(db.String(255))
    is_flagged = db.Column(db.Boolean, default=False)   
    tracks = db.relationship('Track', backref='creator')
    albums = db.relationship('Album', backref='creator')
    playlists = db.relationship('Playlist', backref='creator')
    visits = db.relationship('Visit', backref='user')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def make_creator(self, stage_name, bio, pfp):        
        creator_role = Role.query.filter_by(name='Creator').first()
        self.stage_name = stage_name
        self.bio = bio
        self.pfp_path = pfp
        self.roles.append(creator_role)
        db.session.commit()

    def popularity(self):
        return sum([track.playback_count for track in self.tracks]) if self.tracks else 0

    def get_visited_days(self):
        return len([visit.visit_date for visit in self.visits]) if self.visits else 0

