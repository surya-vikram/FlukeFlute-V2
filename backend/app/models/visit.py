from app.extensions import db
from datetime import datetime

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    visit_date = db.Column(db.Date, default=datetime.utcnow().date)

    @classmethod
    def add_visit_today(cls, user_id):
        today_date = datetime.utcnow().date()
        db.session.add(cls(user_id=user_id, visit_date=today_date))
        db.session.commit()

    @classmethod
    def did_user_visit_today(cls, user_id):
        today_date = datetime.utcnow().date()
        return cls.query.filter_by(user_id=user_id, visit_date=today_date).first() is not None
