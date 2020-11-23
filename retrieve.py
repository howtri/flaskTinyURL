import boto3
from pynamo import Url
from datetime import datetime

ddb_table = boto3.resource('dynamodb', region_name = 'us-east-1').Table('tiny-table')

def retrieve(short_id):
    """
    Accepts the tiny url (short url) and uses get_item (future pynamodb) to retrieve the long url
    returns long_url
    """
    try:
        url = Url.get(short_id)

        url.update(actions=[
            url.hits.set(url.hits + 1),
            url.lastHit.set(datetime.utcnow())
        ])

        return {
            "statusCode": 301,
            "location": url.longURL
        }

    except:
        return 'Error (log)'
