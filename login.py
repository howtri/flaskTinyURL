import jwt
import boto3
import datetime

from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


ddb_table = boto3.resource('dynamodb', region_name='us-east-1').Table('tiny-table-users')
SECRET_KEY = 'hellothereplaintextsecretkey'


class User:
    """Clean up ddb processes and will make future queries + more advanced ops easier"""
    pass
    # make pynamodb model


def jwt_authenticate(func):
    """Wrapper to determine if valid jwt"""
    @wraps(func)
    def inner(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return func(current_user, *args, **kwargs)
    return inner()


def create_user(data):
    """Adds user and hashed password to ddb"""
    hashed_password = generate_password_hash(data['password'], method='sha256')
    ddb_table.put_item(
        Item={
            'username': data['Name'],
            'password': hashed_password,
            'admin': False
        }
    )
    return jsonify({'message': f'User {data["Name"]} created!'}), 200


def login_user(auth):
    """Accepts username and password, compares passed password against stored hash in ddb"""
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Login failed, username or password not supplied'}), 401

    user = ddb_table.get_item(Key={'username': auth.username})
    if not user:
        return jsonify({'message': 'Login failed, invalid username'}), 401
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() +
                            datetime.timedelta(minutes=10)}, SECRET_KEY)

        return jsonify({'token': token.decode('UTF-8')})

    # easier for troubleshooting but it should be changed so they don't know if user or pass is wrong
    return jsonify({'message': 'Login failed, invalid password'}), 401
