from app.models import Language
from flask_restful import Resource, fields, marshal_with
from app.extensions import cache

language_fields = {
    "id": fields.Integer,
    "name": fields.String
}

class LanguagesResource(Resource):
    @cache.cached(1000)
    @marshal_with(language_fields)
    def get(self):
        languages = Language.query.all()
        return languages, 200
