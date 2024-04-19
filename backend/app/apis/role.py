from app.models import Role
from flask_restful import Resource, fields, marshal_with

role_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
}

class RolesResource(Resource):
    @marshal_with(role_fields)
    def get(self):
        roles = Role.query.all()
        return roles, 200
