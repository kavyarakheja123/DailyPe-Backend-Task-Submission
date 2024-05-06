import json
import uuid
import re
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('Users')
manager_table = dynamodb.Table('manager')

def validate_mobile_number(mobile_num):
    # Remove any non-numeric characters
    mobile_num = re.sub(r'\D', '', mobile_num)
    if len(mobile_num) == 10:
        return mobile_num
    elif len(mobile_num) == 12 and mobile_num.startswith('91'): #if a mobile is staring with country code (91) we will remove that
        return mobile_num[2:]
    elif len(mobile_num) == 11 and mobile_num.startswith('0'): #if a mobile number is staring with country code (0) we will remove that
        return mobile_num[1:]
    else:
        return None

def validate_pan_number(pan_num):
    pan_num = pan_num.upper()
    if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_num): #validating pan_number as per defined format for ex:- FDXPR4165AQ is a valid pan_number and FDXPR41Y7Q is invalid
        return pan_num
    else:
        return None

def validate_manager(manager_id):
    response = manager_table.get_item(Key={'manager_id': manager_id}) #checking if the mentioned manager_id is present in manager table or not
    if 'Item' in response:
        return True
    else:
        return False

def lambda_handler(event, context):
    body = json.loads(event['body'])
    full_name = body.get('full_name')
    mob_num = body.get('mob_num')
    pan_num = body.get('pan_num')
    manager_id = body.get('manager_id')

    # Validation of different inputs
    
    if not full_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Full name must not be empty'})
        }
        
    if not mob_num:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Please enter your Mobile Number'})
        }
        
    mob_num = validate_mobile_number(mob_num)
    
    if not mob_num:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid mobile number'})
        }

    #we have used two checks here for validating mobile_number because:-
    # 1.) The first check will validate if the user has entered the mobile number or not
    # 2.) The second check will validate whether the user has entered a valid mobile number or not

    #The same logic applies for validating pan_number below:-
        
    if not pan_num:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Please enter your PAN number'})
        }        
        
    pan_num = validate_pan_number(pan_num)
    
    if not pan_num:
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
            'mob_num': mob_num,
            'pan_num': pan_num,
            'manager_id': manager_id,
            'created_at': str(datetime.utcnow()),
            'updated_at': '',
            'is_active': True
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User created successfully', 'user_id': user_id})
    }

