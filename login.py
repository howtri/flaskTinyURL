import jwt
import boto3
import datetime

from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pynamo import User

ddb_table = boto3.resource('dynamodb', region_name='us-east-1').Table('tiny-table-users')


def jwt_authenticate(func):
    """Wrapper to determine if valid jwt"""
    @wraps(func)
    def inner(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, jwt_get_secret())
            current_user = data['userID']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return func(current_user, *args, **kwargs)
    return inner()


def create_user(data):
    """Adds user and hashed password to ddb"""
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(
        data['Name'],
        password=hashed_password,
        admin=False,
        timeCreated=datetime.datetime.utcnow()
    )

    new_user.save()
    return jsonify({'message': f'User {data["Name"]} created! '}), 200


def login_user(auth):
    """Accepts username and password, compares passed password against stored hash in ddb"""
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Login failed, username or password not supplied'}), 401

    user = User.get(auth.username)
    if not user:
        return jsonify({'message': 'Login failed, invalid username'}), 401
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() +
                            datetime.timedelta(minutes=10)}, jwt_get_secret())

        return jsonify({'token': token.decode('UTF-8')})

    # easier for troubleshooting but it should be changed so they don't know if user or pass is wrong
    return jsonify({'message': 'Login failed, invalid password'}), 401

def jwt_get_secret():
    secret_name = "jwt-secret"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f'encountered exception: {e}')
    else:
        # Decrypts secret using the associated KMS CMK.
        secret = get_secret_value_response['SecretString']
        return secret[14:-2]
