import json
import boto3
from string import ascii_letters, digits
from random import choice, randint
from time import strftime, time
from urllib import parse

string_format = ascii_letters + digits
base_url = 'www.localhost:5000/t/'

ddb_table = boto3.resource('dynamodb', region_name = 'us-east-1').Table('tiny-table')


def create(long_url, id=None):
    """
    Accepts a long url and creates a short url, then maps the two in ddb
    """
    id = generate_id(id)
    short_url = base_url + id
    try:
        response = ddb_table.put_item(
        Item={
            'short_id': id,
            'created_at': generate_timestamp(),
            'short_url': short_url,
            'long_url': long_url,
            'hits': int(0)
        }
    )

    except Exception as e:
        print(f'Error {e}')

    return {
        "statusCode": 200,
        "body": short_url
    }

def generate_timestamp():
    response = strftime("%Y-%m-%dT%H:%M:%S")
    return response

def check_id(short_id):
    if 'Item' in ddb_table.get_item(Key={'short_id': short_id}):
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

# if __name__ == '__main__':
#     create('google.com')