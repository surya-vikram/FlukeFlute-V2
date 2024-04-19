from flask import abort
import re
from app.models import *

def validate_email(email):
    if not email:
        abort(400, 'Email is required')
    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not re.match(email_pattern, email):
        abort(400, 'Invalid email format')

def validate_name(name):
    if not name:
        abort(400, 'Name field is empty')
    if not name.replace(' ', '').isalpha():
        abort(400, 'Only letters and spaces allowed in the name.')

def validate_username(username):
    if not username:
        abort(400, 'You must give username')
    if not (username.isalnum() or '_' in username):
        abort(400, 'Only letters, numbers, and underscores allowed in the username.')

def validate_unique_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        abort(400, 'This username is already taken. Please choose a different username.')

def validate_unique_email(email):
    email_address = User.query.filter_by(email=email).first()
    if email_address:
        abort(400, 'This email address is already registered. Please use a different email address.')

def validate_password(password):
    if not password:
        abort(400, 'Password is required')
    if len(password) < 8:
        abort(400, description='Password too small. Must have at least 8 characters.')
    if ' ' in password:
        abort(400, description='Password cannot contain white spaces.')



