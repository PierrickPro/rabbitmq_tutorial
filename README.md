# RabbitMQ Tutorial

This repository is what I learned while following the YouTube playlist [RabbitMQ Tutorial](https://www.youtube.com/playlist?list=PLalrWAGybpB-UHbRDhFsBgXJM1g6T4IvO) by jumpstartCS.

## Setting up RabbitMQ with Docker

To get started, follow these steps to set up RabbitMQ using Docker:

1. Install RabbitMQ Docker image:
    ```
    docker pull rabbitmq:3.9-management
    ```

2. Run the Docker image:
    ```
    docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
    ```

3. Access the RabbitMQ management plugin by visiting:
    [http://localhost:15672/#/](http://localhost:15672/#/)

4. Use the following default administrator credentials:
    - Username: guest
    - Password: guest

## Competing Consumers

This section demonstrates the concept of competing consumers using RabbitMQ. Here's how it works:

1. The producer generates messages at random intervals ranging from 1 to 4 seconds
2. The consumer processes messages with a processing time at random intervals ranging from 1 to 6 seconds

This leads to a scenario where the production of messages is faster than their consumption

- When running a single consumer and producer, you'll quickly notice that the consumer is unable to keep up with the production rate

- However, by adding a second consumer, you'll observe that consumption now matches the production rate

- Pay attention to the `prefetch_count` set to 1. The `prefetch_count` setting is used to control how many unacknowledged messages a consumer can have at a time. This means that when a consumer is still processing a message, the next message is assigned to an available consumer

- If you omit setting the `prefetch_count`, the default round-robin algorithm distributes messages. Running 2 consumers without specifying the `prefetch_count` will result in one consumer processing messages with even message IDs, while the other handles odd message IDs

## Pub-Sub

- For this setup, the producer publishes messages to a fanout exchange without knowledge of queues.


- Consumers:
  - bind the fanout exchange to its channel
  - You don't need to specify a queue name, the server generates a queue name automatically
  - This queue is exclusive, so the server can close it when unused
  - Consumer2 deliberately avoids binding the exchange to its channel


- Only consumer1 receives a message when the producer is executed. This outcome is because consumer1 is the only consumer bound to the exchange.


- This Publisher-Subscriber setup allows consumers to subscribe to relevant exchanges without the producer needing to know the specifics of consumer queues. The messages can now be delivered to multiple consumers via different queues.

## Routing

- Producers publish messages to a direct exchange and with a designated routing key


- Consumers:
    - Similar to the publish-subscribe model, consumers bind their channels to the exchange
    - Each consumer specifies a different routing_key: payments_only and analytics_only
    - Both consumers have the both_consumers routing key


- Only the consumers with a matching routing key will receive the messages sent by the producer

## Topics

Topics enable more flexible routing using topic-based routing keys

- Routing keys can be structured like topics, allowing for powerful message filtering:
  - \* (star) can substitute for exactly one word
  - \# (hash) can substitute for zero or more words

Here are some scenarios:

- Consumers: 
  - consumer1: **_routing_key='user.#'_**
  - consumer2: **_routing_key='*.europe.*'_**
  - consumer3: **_routing_key='#.payments'_**


- Scenarios
  - **_routing_key='user.europe.payments'_**  &rarr; all 3 consumers will receive the message
  - **_routing_key='business.europe.order'_**  &rarr; only consumer2 will receive the message

## Request Response Pattern

The Request response patterns allows two applications to have a two-way conversation with one another.
This is common in client-server architecture.

- Client:
  - publishes messages to a request queue
  - properties containing the name of the reply queue and correlation_id are passed with the message
  - consumes response from the reply_queue

- Server:
  - consumes messages from the request queue
  - extract reply_queue name and correlation_id from the properties in the message
  - publishes response message in the reply_queue

## Exchange-Exchange

A message can go through multiple exchanges.

- Producer:
  - declare exchanges
  - bind the exchanges together
  - publish to the first exchange

- Consumer:
  - declare last exchange
  - declare a queue
  - bind the queue to the last exchange
  - consume from the queue

The message will now go through the two exchanges.

## Headers Exchange

A header exchange can also be used. 
A header exchange is a routing system that uses arguments with headers and optional values to route messages.

- Producer:
  - declare headers_exchange of type headers
  - add headers in the properties when publishing the message


- Consumer:
  - declare headers_exchange
  - declare a queue
  - bind the queue to the headers_exchange and set arguments
  - consume from the queue

We can now leverage the power of arguments to route messages.

- Binding Arguments:
  - 'x-match': 'any' &rarr; any argument can match
  - 'x-match': 'all' &rarr; all arguments need to match

## Alternate Exchange

An alternate exchange can be used to route all messages that can't be delivered through the main exchange.

- Producer:
  - declare the alternate exchange
  - declare the main exchange, with the alternate exchange name in the arguments
  - publish the message with a routing key


- Consumer:
  - Alternative:
    - declare alternative queue
    - declare alternative exchange
    - bind queue to the exchange
    - consume from the queue, with on_message_callback=alt_queue_on_message_received
  - Main:
    - declare main queue
    - declare main exchange
    - bind queue to the exchange with a routing_key
    - consume from the queue, with on_message_callback=main_queue_on_message_received

Run the consumer and the producer.
If the routing key of the main consumer matches they producer's key, the message is delivered in the main queue.
If there is no match, the message is delivered in the alternate queue.


