import pika
import json

# Set up connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Declare exchange and queue
# exchange_name = 'health'
# health_check_queue = 'health_check'
channel.exchange_declare(exchange='health', exchange_type='direct')
channel.queue_declare(queue='health_check')
channel.queue_bind(exchange='health', queue='health_check', routing_key='health_check')

# Define callback function
def callback(ch, method, properties, body):
    data = str(body, 'utf-8')
    print(f" [H] Received message: {data}",flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages from queue
channel.basic_consume(queue='health_check', on_message_callback=callback)

# Start consuming messages
channel.start_consuming()
