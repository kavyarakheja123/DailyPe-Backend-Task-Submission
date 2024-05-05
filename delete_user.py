import boto3
import json

def delete_user(user_id=None, mob_num=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    if user_id:
        response = table.delete_item(Key={'user_id': user_id})
        if 'Attributes' not in response:
            return {'message': 'User not found'}
    elif mob_num:
        response = table.scan(FilterExpression='mob_num = :mob_num',
                              ExpressionAttributeValues={':mob_num': mob_num})
        items = response.get('Items', [])
        if not items:
            return {'message': 'User not found'}
        for item in items:
            table.delete_item(Key={'user_id': item['user_id']})

    return {'message': 'User deleted successfully'}

def lambda_handler(event, context):
    body = json.loads(event['body'])

    # Extract user_id or mob_num from the request body
    user_id = body.get('user_id')
    mob_num = body.get('mob_num')

    # Check if either user_id or mob_num is provided
    if not user_id and not mob_num:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Either user_id or mob_num must be provided'})
        }

    # Delete user based on user_id or mob_num
    response = delete_user(user_id, mob_num)

    # Return the response
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
