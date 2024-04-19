from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from app.models import User, Visit
from flask import abort, jsonify, make_response
from config import Config
from app.extensions import cache

class UserLogin(Resource):
    def post(self):
        cache.clear()
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()
        username, password = args['username'], args['password']
        if not username:
            abort(400, 'Username is empty')
        if not password:
            abort(400, 'Password is needed')
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404, 'User not found')
        if not user.check_password_correction(password):
            abort(401, 'Invalid credentials')
        user_roles = [ role.name for role in user.roles ]
        if 'Basic' not in user_roles:
            abort(403, 'User is not authorized')
        if not Visit.did_user_visit_today(user.id):
            Visit.add_visit_today(user.id)
        token_expires = Config().JWT_ACCESS_TOKEN_EXPIRES
        access_token = create_access_token(identity=user.id, expires_delta=token_expires)
        return {'user_id': user.id, 'roles': user_roles, 'access_token': access_token}, 200


class AdminLogin(Resource):
    def post(self):
        cache.clear()
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()
        username, password = args['username'], args['password']
        if not username:
            abort(400, 'Username is empty')
        if not password:
            abort(400, 'Password is needed')
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404, 'User not found')
        if not user.check_password_correction(password):
            abort(401, 'Invalid credentials')
        user_roles = [ role.name for role in user.roles ]
        if 'Admin' not in user_roles:
            abort(403, 'User is not authorized')
        token_expires = Config().JWT_ACCESS_TOKEN_EXPIRES
        access_token = create_access_token(identity=user.id, expires_delta=token_expires)
        return {'user_id': user.id, 'roles': user_roles, 'access_token': access_token}, 200
    
    
