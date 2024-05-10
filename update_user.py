import boto3
import json
import uuid
import re
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('Users') 
managers_table = dynamodb.Table('manager') 

def validate_mobile_number(mobile_num):
    # Remove any non-numeric characters
    mobile_num = re.sub(r'\D', '', mobile_num)
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
    response = managers_table.get_item(Key={'manager_id': manager_id})
    if 'Item' in response:
        return True
    else:
        return False

def update_user(user_ids, update_data):
    for user_id in user_ids:
        # Check if user exists
        response = users_table.get_item(Key={'user_id': user_id})
        if 'Item' not in response:
            continue  # Skip updating non-existent user

        # Extract existing user data
        user_data = response['Item']

        # Validate and update data
        updated_data = {}
        for key, value in update_data.items():
            if key == 'mob_num':
                if not validate_mobile_number(value):
                    return {'error': 'Invalid mobile number'}
                updated_data[key] = value
            elif key == 'pan_num':
                if not validate_pan_number(value):
                    return {'error': 'Invalid PAN number'}
                updated_data[key] = value 
            elif key == 'manager_id':
                if not validate_manager(value):
                    return {'error': 'Invalid manager_id'}
                updated_data[key] = value 
            else:
                updated_data[key] = value
                
                
        if updated_data:
            # If manager_id is being updated
            if 'manager_id' in updated_data:
                if 'manager_id' in user_data:
                    # Deactivate current user entry
                    users_table.update_item(
                        Key={'user_id': user_id},
                        UpdateExpression='SET is_active = :false, updated_at = :updated_at',
                        ExpressionAttributeValues={':false': False, ':updated_at': str(datetime.utcnow())}
                    )
                    
                    user_data['manager_id'] = updated_data['manager_id']
                    user_data.update(updated_data)
                    
                    new_user_id = str(uuid.uuid4())
                    
                    users_table.put_item(
                        
                        Item ={
                            'user_id' : new_user_id,
                            'full_name': user_data['full_name'],
                            'mob_num': user_data['mob_num'],
                            'pan_num': user_data['pan_num'],
                            'manager_id': user_data['manager_id'],
                            'created_at': user_data['created_at'],
                            'is_active' : True,
                            'updated_at': str(datetime.utcnow())
                        }
                    )
                    
                    
                else:
                    user_data['manager_id'] = updated_data['manager_id']
                    user_data['updated_at'] = str(datetime.utcnow())
                    

    return {'message': 'Users updated successfully'}

def lambda_handler(event, context):
    body = json.loads(event['body'])

    # Extract user_ids and update_data from the request body
    user_ids = body.get('user_ids', [])
    update_data = body.get('update_data', {})

    # Check if user_ids or mob_nums are provided
    if not user_ids:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No user_ids provided'})
        }
        
    update_keys = set(update_data.keys())

    if len(user_ids)>1 :
        if update_keys == {'manager_id'}:
            if not validate_manager(update_data['manager_id']):
                return {'error': 'Invalid manager_id'} 
        
        else : 
            return {'error': 'Extra keys found. Only individual updates allowed.'}
            

    # Update users
    response = update_user(user_ids, update_data)

    # Return the response
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
