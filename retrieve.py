import boto3

ddb_table = boto3.resource('dynamodb', region_name = 'us-east-1').Table('tiny-table')

def retrieve(short_id):
    """
    Accepts the tiny url (short url) and uses get_item (future pynamodb) to retrieve the long url
    returns long_url
    """
    try:
        item = ddb_table.get_item(Key={'short_id': short_id})
        long_url = item.get('Item').get('long_url')

        ddb_table.update_item(
            Key={'short_id': short_id},
            UpdateExpression='set hits = hits + :val',
            ExpressionAttributeValues={':val': 1}
        )

    except:
        # return {
        #     'statusCode': 301,
        #     'location': 'https://objects.ruanbekker.com/assets/images/404-blue.jpg'
        # }
        print('Error (log)')

    return {
        "statusCode": 301,
        "location": long_url
    }

if __name__ == '__main__':
    print(retrieve('iRBq'))