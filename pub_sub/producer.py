import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

message = "Hello I want to broadcast this message"
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)
# publish to fanout exchange
channel.basic_publish(exchange='pubsub', routing_key='', body=message)

print(f"sent message: {message}")
connection.close()