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

1. The producer generates messages at random intervals ranging from 1 to 4 seconds.
2. The consumer processes messages with a processing time at random intervals ranging from 1 to 6 seconds.

This leads to a scenario where the production of messages is faster than their consumption.

- When running a single consumer and producer, you'll quickly notice that the consumer is unable to keep up with the production rate.

- However, by adding a second consumer, you'll observe that consumption now matches the production rate. 

- Pay attention to the `prefetch_count` set to 1. The prefetch_count setting is used to control how many unacknowledged messages a consumer can have at a time. This means that when a consumer is still processing a message, the next message is assigned to an available consumer.

- If you omit setting the `prefetch_count`, the default round-robin algorithm distributes messages. Running 2 consumers without specifying the `prefetch_count` will result in one consumer processing messages with even message IDs, while the other handles odd message IDs.

