from app.models import Genre
from flask_restful import Resource, fields, marshal_with
from app.extensions import cache

genre_fields = {
    "id": fields.Integer,
    "name": fields.String
}

class GenresResource(Resource):
    @cache.cached(1000)
    @marshal_with(genre_fields)
    def get(self):
        genres = Genre.query.all()
        return genres, 200
