from flask import Flask, request, jsonify, redirect
from retrieve import retrieve
from create import create

app = Flask(__name__)

@app.route('/', methods=['GET'])
def query_records():
    name = request.args.get('name')
    print(name)
    try:
        return jsonify('error1')
    except:
        return jsonify('error')

@app.route('/t/', methods=['GET'])
def retrieve_long():
    short_url = request.args.get('short_url')
    long_response = retrieve(short_url)
    print(long_response['location'])
    #return redirect(long_response['location'], long_response['statusCode'])
    return long_response

@app.route('/create/', methods=['POST'])
def create():
    long_url = request.args.get('long_url')
    print(long_url)
    short_response = create(long_url)
    print(short_response['body'])
    return short_response

app.run()