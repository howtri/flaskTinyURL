import boto3
from string import ascii_letters, digits
from random import choice, randint
from datetime import datetime
from pynamo import Url

string_format = ascii_letters + digits
ddb_table = boto3.resource('dynamodb', region_name='us-east-1').Table('tiny-table')


def create(long_url, current_user, url_id=None):
    """
    Accepts a long url and creates a short url, then maps the two in ddb
    """
    url_id = generate_id(id)

    new_tiny = Url(
        url_id,
        longURL=long_url,
        timeCreated=datetime.utcnow(),
        hits=0,
        creator=current_user
    )

    new_tiny.save()

    base_url = 'www.localhost:5000/t/'
    return {
        "statusCode": 200,
        "body": base_url + url_id
    }

def check_id(short_id):
    # does this query the global index?
    if short_id in Url.shortID.query():
        return generate_id(None)
    else:
        return short_id

def generate_id(short_id):
    if short_id is None:
        short_id = "".join(choice(string_format) for x in range(4))
        print(f'{short_id} generated')
    print('Checking ' + short_id)
    response = check_id(short_id)
    return response
