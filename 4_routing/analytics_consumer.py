import pika
from pika.exchange_type import ExchangeType

def on_message_received(ch, method, properties, body):
    print(f"Analytics Service - received new message: {body}")

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.exchange_declare(exchange='4_routing', exchange_type=ExchangeType.direct)
queue = channel.queue_declare(queue='', exclusive=True)
# queue binding with a 4_routing key
channel.queue_bind(exchange='4_routing', queue=queue.method.queue, routing_key='analytics_only')
channel.queue_bind(exchange='4_routing', queue=queue.method.queue, routing_key='both')

channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print("Starting Consuming")

channel.start_consuming()