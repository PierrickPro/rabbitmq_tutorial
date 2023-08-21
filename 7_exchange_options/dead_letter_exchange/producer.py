import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.exchange_declare(exchange='main_exchange', exchange_type=ExchangeType.direct)
message = "This message will expire..."
channel.basic_publish(exchange='main_exchange', routing_key="test", body=message)

print(f"sent message: {message}")
connection.close()
