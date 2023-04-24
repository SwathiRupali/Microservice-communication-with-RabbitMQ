import pika
import json
import pymongo

# Set up connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

# Declare exchange and queue
exchange_name = 'message_exchange'
delete_record_queue = 'delete_record'
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
channel.queue_declare(queue=delete_record_queue)
channel.queue_bind(exchange=exchange_name, queue=delete_record_queue, routing_key=delete_record_queue)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://host.docker.internal:27017")
db = client['mydatabase']
collection = db['students']

# Define callback function
def callback(ch, method, properties, body):
    srn = str(body, 'utf-8')
    result = collection.delete_one({'SRN': srn})
    print(f" [D] Deleted {result.deleted_count} record(s) with SRN: {srn}",flush=True)
    channel.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages from queue
channel.basic_consume(queue=delete_record_queue, on_message_callback=callback)

# Start consuming
channel.start_consuming()
