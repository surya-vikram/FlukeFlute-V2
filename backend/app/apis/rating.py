from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity
from app.models import Rating
from app.utils import role_required
from flask import request
from app.extensions import db, cache
from sqlalchemy import and_


class RatingResource(Resource):
    @role_required('Basic')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('track_id')
        parser.add_argument('rating_value')
        args = parser.parse_args()
        track_id, rating_value = args.get('track_id'), int(args.get('rating_value'))
        user_id = get_jwt_identity()
        existing_rating = Rating.query.filter(and_(Rating.user_id == user_id, Rating.track_id == track_id)).first()
        if existing_rating:
            existing_rating.rating_value = rating_value
            db.session.commit()
            cache.clear()
            return {'message': 'Rating updated successfully'}, 200
        rating = Rating(user_id=user_id, track_id=track_id, rating_value=rating_value)
        db.session.add(rating)
        db.session.commit()
        cache.clear()
        return {'message': 'Thanks for rating the track!'}, 200

    

    