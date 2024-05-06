import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('manager')


def add_manager(manager_name):
    # Validate manager's name
    if not manager_name:
        return {'error': 'Manager name is required'}

    # Generate UUID for the manager
    manager_id = str(uuid.uuid4())

    created_at = str(datetime.utcnow())

    table.put_item(Item={'manager_id': manager_id, 'manager_name': manager_name, 'created_at': created_at})

    return {'message': 'Manager added successfully', 'manager_id': manager_id}

def lambda_handler(event, context):
  
    body = json.loads(event['body'])
    manager_name = body.get('manager_name')
  
    response = add_manager(manager_name)

    return response
