from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User
from flask import jsonify

def role_required(role_name):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if role_name not in [role.name for role in user.roles]:
                return jsonify({'message': 'Unauthorized access'}), 403
            return func(*args, **kwargs)
        return decorated_view
    return wrapper

