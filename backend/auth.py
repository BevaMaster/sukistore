import jwt
from functools import wraps
from flask import request, jsonify
from passlib.hash import bcrypt
from models import User, db

SECRET_KEY = 'changeme_supersecret'  # ganti sebelum deploy

def hash_password(password):
    return bcrypt.hash(password)

def verify_password(password, pw_hash):
    return bcrypt.verify(password, pw_hash)

def generate_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except Exception:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
