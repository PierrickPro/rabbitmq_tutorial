import pika
import uuid


def on_reply_message_received(ch, method, properties, body):
    print(f"reply received: {body}")


connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.queue_declare(queue='', exclusive=True)
reply_queue = channel.queue_declare(queue='', exclusive=True)

# client consumes with an on_reply callback
channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True, on_message_callback=on_reply_message_received)
channel.queue_declare(queue='request-queue')

message = "Can I request a reply?"
cor_id = str(uuid.uuid4())
print(f"Sending Request: {cor_id}")

# client also publishes with a basic property giving details on what reply queue to use and setting a correlation_id
channel.basic_publish(exchange='', routing_key='request-queue',
                      properties=pika.BasicProperties(
                          reply_to=reply_queue.method.queue,
                          correlation_id=cor_id
                      ),
                      body=message)

print(f"Starting Client")
channel.start_consuming()
