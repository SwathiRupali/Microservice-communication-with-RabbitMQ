import pika
import json
import pymongo

# Set up connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

# Declare exchange and queue
exchange_name = 'message_exchange'
insert_record_queue = 'insert_record'
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
channel.queue_declare(queue=insert_record_queue)
channel.queue_bind(exchange=exchange_name, queue=insert_record_queue, routing_key=insert_record_queue)

# Connect to MongoDB
client =  pymongo.MongoClient("mongodb://host.docker.internal:27017")
db = client['mydatabase']
collection = db['students']

# Define callback function
def callback(ch, method, properties, body):
    data = json.loads(body)
    collection.insert_one(data)
    print(f" [I] Inserted record: {data}",flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages from queue
channel.basic_consume(queue=insert_record_queue, on_message_callback=callback)

# Start consuming messages
channel.start_consuming()
