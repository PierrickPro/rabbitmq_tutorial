import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.exchange_declare(exchange="exchange1", exchange_type=ExchangeType.direct)
channel.exchange_declare(exchange="exchange2", exchange_type=ExchangeType.fanout)
# where it's going to first argument, where it's coming form second argument
channel.exchange_bind("exchange2", "exchange1")

message = "This message has gone through multiple exchanges"
channel.basic_publish(exchange='exchange1', routing_key='', body=message)

print(f"sent message: {message}")
connection.close()