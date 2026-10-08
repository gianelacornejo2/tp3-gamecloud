import json
import os
import boto3

sqs = boto3.client('sqs', region_name='us-east-1')
QUEUE_URL = os.environ.get('QUEUE_URL')
JUEGOS_VALIDOS = ['doom', 'pacman']

def handler(event, context):
    try:
        body = event.get('body')
        if isinstance(body, str):
            data = json.loads(body)
        elif isinstance(body, dict):
            data = body
        else:
            data = {}

        jugador = data.get('jugador')
        juego = data.get('juego')
        puntaje = data.get('puntaje')

        if not jugador or not isinstance(jugador, str):
            return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"}, "body": json.dumps({"error": "Jugador invalido"})}

        if juego not in JUEGOS_VALIDOS:
            return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"}, "body": json.dumps({"error": "Juego invalido"})}

        if puntaje is None or not isinstance(puntaje, int) or isinstance(puntaje, bool):
            return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"}, "body": json.dumps({"error": "Puntaje debe ser un entero"})}

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({"jugador": jugador, "juego": juego, "puntaje": puntaje})
        )

        return {
            "statusCode": 202,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"status": "Accepted"})
        }
    except Exception as e:
        return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"}, "body": json.dumps({"error": str(e)})}
