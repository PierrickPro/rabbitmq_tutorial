import pika
from pika.exchange_type import ExchangeType

def on_message_received(ch, method, properties, body):
    print(f"consumer2 received new message: {body}")

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
# exchange is declared in case it hasn't been declared yet
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)
queue = channel.queue_declare(queue='', exclusive=True)
# the queue is not bound to the channel in consumer2
# channel.queue_bind(exchange='pubsub', queue=queue.method.queue)
channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print("Starting Consuming")

channel.start_consuming()