import pika

# Establish a connection to RabbitMQ
credential = pika.PlainCredentials("rabbitmq", "rabbitmq")
connection = pika.BlockingConnection(pika.ConnectionParameters("103.157.218.126", port=40000, credentials=credential))
channel = connection.channel()

# Declare a queue for the server to listen for requests
channel.queue_declare(queue="rpc_queue")


# Define a function to handle requests and return responses
def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fibonacci(n)

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(response),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# Consume requests
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="rpc_queue", on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
