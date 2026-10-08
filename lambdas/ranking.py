import json
import os
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'Puntajes'))

def handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    juego_filtro = query_params.get('juego')

    response = table.scan()
    items = response.get('Items', [])

    for item in items:
        item['puntaje'] = int(item['puntaje'])

    if juego_filtro:
        items = [item for item in items if item.get('juego') == juego_filtro]

    items.sort(key=lambda x: x['puntaje'], reverse=True)
    top_10 = items[:10]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(top_10)
    }
