import json
import uuid
import re
import boto3

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('UserTable')
manager_table = dynamodb.Table('manager')

def validate_mobile_number(mobile_num):
    if len(mobile_num) == 10:
        return mobile_num
    elif len(mobile_num) == 12 and mobile_num.startswith('91'):
        return mobile_num[2:]
    elif len(mobile_num) == 11 and mobile_num.startswith('0'):
        return mobile_num[1:]
    else:
        return None

def validate_pan_number(pan_num):
    pan_num = pan_num.upper()
    if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_num):
        return pan_num
    else:
        return None

def validate_manager(manager_id):
    response = manager_table.get_item(Key={'manager_id': manager_id})
    if 'Item' in response:
        return True
    else:
        return False

def lambda_handler(event, context):
    body = json.loads(event['body'])
    full_name = body.get('full_name')
    mob_number = body.get('mob_number')
    pan_num = body.get('pan_number')
    manager_id = body.get('manager_id')

    # Validation of different inputs
    if not full_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Full name must not be empty'})
        }
        
    if not mob_number:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid mobile number'})
        }
    mob_number = validate_mobile_number(mob_number)
    
    if not mob_number:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid mobile number'})
        }
    
    if not pan_number:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid PAN number'})
        }
        
        
    pan_number = validate_pan_number(pan_num)
    
    if not pan_number:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid PAN number'})
        }
    
    if manager_id and not validate_manager(manager_id):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid manager ID'})
        }

    # Insert user data into DynamoDB
    user_id = str(uuid.uuid4())
    
    user_table.put_item(
        Item={
            'user_id': user_id,
            'full_name': full_name,
            'mob_number': mob_number,
            'pan_number': pan_number,
            'manager_id': manager_id,
            # 'created_at': str(datetime.utcnow()),
            # 'updated_at': '',
            'is_active': True
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User created successfully', 'user_id': user_id})
    }
