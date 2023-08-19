import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.exchange_declare(exchange='my_topic_exchange', exchange_type=ExchangeType.topic)

user_payment_message = 'A european user paid for something'
channel.basic_publish(exchange='my_topic_exchange', routing_key='user.europe.payments', body=user_payment_message)
print(f"sent message: {user_payment_message}")


business_order_message = 'A european business placed an order'
channel.basic_publish(exchange='my_topic_exchange', routing_key='business.europe.order', body=business_order_message)
print(f"sent message: {business_order_message}")

connection.close()