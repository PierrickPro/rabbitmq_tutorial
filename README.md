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

Implementing the pub-sub messaging pattern with a fanout exchange.

- For this setup, the producer publishes messages to a fanout exchange without knowledge of queues.


- Consumer1 binds the same exchange to its channel
  - You don't need to specify a queue name
  - The server generates a queue name automatically
  - This queue is exclusive, and the server can close it when unused


- Consumer2 deliberately avoids binding the exchange to its channel


- With both consumers running, you'll notice that only consumer1 receives a message when the producer is executed. This outcome is because consumer1 is the only consumer bound to the exchange.


- This Publisher-Subscriber setup demonstrates RabbitMQ's flexibility in managing message routing, allowing consumers to subscribe to relevant exchanges without the producer needing to know the specifics of consumer queues. The messages can now be delivered to multiple consumers via different queues.

## Routing

### Direct Exchange

Implementing routing with a direct exchange.

- Producers publish messages to a direct exchange using a designated routing key

- Consumers:
    - Similar to the publish-subscribe model, consumers bind their channels to the exchange
    - Each consumer specifies a different routing_key: payments_only and analytics_only
    - Both consumers have the both_consumers routing key


- Only the consumers with a matching routing key will receive the messages sent by the producer

### Topic Exchange

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


