import pika
from pika.exchange_type import ExchangeType


def dlx_queue_on_message_received(ch, method, properties, body):
    print(f"DLX: received new message: {body}")


def main_queue_on_message_received(ch, method, properties, body):
    print(f"Main: received new message: {body}")


connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

# main exchange queue
channel.exchange_declare(exchange='main_exchange', exchange_type=ExchangeType.direct)
channel.queue_declare(queue='main_exchange_queue',
                      arguments={'x-dead-letter-exchange': 'dlx', 'x-message-ttl': 1000})
channel.queue_bind('main_exchange_queue', 'main_exchange', 'test')
# When main exchange queue has no consumer, the messages are moved to the dlx queue
# channel.basic_consume(queue='main_exchange_queue', auto_ack=True, on_message_callback=main_queue_on_message_received)

# dead letter exchange queue
channel.exchange_declare(exchange='dlx', exchange_type=ExchangeType.fanout)
channel.queue_declare(queue='dlx_queue')
channel.queue_bind('dlx_queue', 'dlx')
channel.basic_consume(queue='dlx_queue', auto_ack=True, on_message_callback=dlx_queue_on_message_received)

print("Starting Consuming")
channel.start_consuming()
