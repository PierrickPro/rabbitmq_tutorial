import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.exchange_declare(exchange='4_routing', exchange_type=ExchangeType.direct)

message = 'This message needs to be routed'
channel.basic_publish(exchange='4_routing', routing_key='both', body=message)

print(f"sent message: {message}")

connection.close()