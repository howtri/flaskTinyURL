from flask import Flask, request, jsonify, redirect, render_template
from retrieve import retrieve
from urls import create
from login import create_user, jwt_authenticate, login_user

app = Flask(__name__)

# https://www.youtube.com/watch?v=J5bIPtEbS0Q

@app.route('/')
def index():
    return render_template('start.html')

@app.route('/t/<short_id>', methods=['GET'])
@jwt_authenticate
# maybe rate limit to 100 requests every 30 min
def retrieve_long(current_user, short_id):
    short_url = request.args.get('short_url')
    long_response = retrieve(short_url)
    print(long_response['location'])
    #return redirect(long_response['location'], long_response['statusCode'])
    return long_response

@app.route('/url/', methods=['POST'])
@jwt_authenticate
# maybe limit to 10 creations per day
# add in optional id for url name
def create(current_user):
    long_url = request.args.get('long_url')
    print(long_url)
    # look at getting current_user from jwt_authenticate
    short_response = create(long_url, jwt_authenticate.current_user)
    print(short_response['body'])
    return short_response
    # return render_template('yourURLs.html')

@app.route('/url/', methods=['DELETE'])
@jwt_authenticate
# admin can delete urls... or also user?
def create(current_user):
    pass

@app.route('/admin/', methods=['PUT'])
@jwt_authenticate
def set_admin(current_user):
    if current_user.admin:
        pass
    pass

@app.route('/signup/', methods=['POST'])
def sign_up():
    user_info = request.get_json()
    return create_user(user_info)

@app.route('/login/', methods=['POST'])
def login():
    # does this also need to be get_json?
    auth_info = request.authorization
    return login_user(auth_info)

app.run()
