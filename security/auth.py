import jwt
import datetime
from functools import wraps
from flask import request, jsonify 
from jwt import ExpiredSignatureError, InvalidTokenError

#key 
SECRET_KEY="9876543210"

#generate token
def generate_token(user_id):
    #payload
    payload = {
        "user_id" : user_id,
        #expired time
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        "iat" : datetime.datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

#decode token
def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')


#middleware require_auth (using cookies)
def require_auth(f):
    @wraps(f)
    def wrapper(*args , **kwargs):
        #receive token from request
        token = request.cookies.get("auth_token")

        if not token:
            return jsonify({
                'status': 1,
                'errorMessage': 'Not  authenticated'
            }),401
        try:
            decoded = decode_token(token)
            #Save user_id in request
            request.user_id = decoded.get("user_id")
        except ExpiredSignatureError:
            return jsonify({
                'status': 1,
                'errorMessage': 'Session expired'
            }),401
        except InvalidTokenError:
            return jsonify({
                'status': 1,
                'errorMessage':'Invalid session'
            }),401
        return f(*args, **kwargs)

    return wrapper

#middleware require_auth
'''
def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        #receive token from request
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({
                "status" : 1,
                "errorMessage" : "token missing"
            }),401

        #remove "bearer"  prefix
        token = token.replace("Bearer ", "").strip()
        try:
            decoded = decode_token(token)
            #save user_id in request
            request.user_id = decoded.get("user_id")
        except ExpiredSignatureError: 
            return jsonify({
                "status" : 1,
                "errorMessage" : "token expired"
            }),401
        except InvalidTokenError: 
            return jsonify({
                "status" : 1,
                "errorMessage" : "invalid token"
            }),401
        except Exception as e: 
            return jsonify({
                "status" : 1,
                "errorMessage" : "auth error"
            }),401
        return f(*args, **kwargs)
    return wrapper

'''