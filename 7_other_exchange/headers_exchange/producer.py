import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.exchange_declare(exchange="headers_exchange", exchange_type=ExchangeType.headers)
message = "This message will be sent with headers"
channel.basic_publish(
    exchange='headers_exchange',
    routing_key='',
    body=message,
    properties=pika.BasicProperties(headers={'name': 'brian'}))

print(f"sent message: {message}")
connection.close()
