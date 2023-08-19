import pika
import time
import random

def on_message_received(ch, method, properties, body):
    processing_time = random.randint(1, 6)
    print(f"received new message: {body}, will take {processing_time}s to process")
    time.sleep(processing_time)
    # ACK is sent after waiting a random number of seconds
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Finished processing the message")

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.queue_declare(queue='letterbox')

# consumer will only process a single message at a time
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='letterbox', on_message_callback=on_message_received)
print("Starting Consuming")
channel.start_consuming()