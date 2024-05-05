import boto3
import json
from boto3.dynamodb.conditions import Key

def get_users(event):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    # Parse request body
    body = json.loads(event['body'])
    mob_num = body.get('mob_num')
    user_id = body.get('user_id')
    manager_id = body.get('manager_id')

    if user_id:
        response = table.query(KeyConditionExpression=Key('user_id').eq(user_id))
    elif mob_num:
        response = table.scan(FilterExpression=Key('mob_num').eq(mob_num))
    elif manager_id:
        response = table.scan(FilterExpression=Key('manager_id').eq(manager_id))
    else:
        response = table.scan()

    users = response.get('Items', [])

    # Format the response
    formatted_users = []
    for user in users:
        formatted_user = {
            'user_id': user['user_id'],
            'manager_id': user.get('manager_id', ''),
            'full_name': user['full_name'],
            'mob_num': user['mob_num'],
            'pan_num': user['pan_num'],
            'created_at': user['created_at'],
            'updated_at': user.get('updated_at', ''),
            'is_active': user['is_active']
        }
        formatted_users.append(formatted_user)

    return formatted_users

def lambda_handler(event, context):
    # Retrieve users based on the specified criteria
    users = get_users(event)

    # Return the response
    return {
        'statusCode': 200,
        'body': json.dumps({'users': users})
    }
