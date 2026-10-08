import json
import os
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'Puntajes'))

def handler(event, context):
    for record in event.get('Records', []):
        body_str = record.get('body', '')
        data = json.loads(body_str)

        jugador = data['jugador']
        juego = data['juego']
        nuevo_puntaje = int(data['puntaje'])

        res = table.get_item(Key={'juego': juego, 'jugador': jugador})
        item = res.get('Item')

        if not item or nuevo_puntaje > int(item.get('puntaje', 0)):
            table.put_item(
                Item={
                    'juego': juego,
                    'jugador': jugador,
                    'puntaje': nuevo_puntaje
                }
            )
            print(f"Puntaje actualizado para {jugador} en {juego}: {nuevo_puntaje}")
        else:
            print(f"Puntaje descartado ({nuevo_puntaje} no supera {item.get('puntaje')})")

    return {"status": "ok"}
