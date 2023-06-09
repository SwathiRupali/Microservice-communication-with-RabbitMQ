import pika
import pymongo

# RabbitMQ connection and channel objects
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

# Declare the exchange and queue
# rabbitmq_exchange = 'read'
# rabbitmq_queue = 'read_database'
channel.exchange_declare(exchange='read', exchange_type="direct")
channel.queue_declare(queue='read_database')
channel.queue_bind(exchange='read', queue='read_database', routing_key='read_database')

# MongoDB database and collection objects
client = pymongo.MongoClient("mongodb://host.docker.internal:27017")
db = client['mydatabase']
collection = db['students']

def read_from_db():
    results = collection.find()
    data = []
    for document in results:
        document['_id'] = str(document['_id'])
        data.append(document)
    return data

# Callback function that is called when a message is received from RabbitMQ
def callback(ch, method, properties, body):
    result = read_from_db()
    for i in range(len(result)):
        print(" [R] Reading Database "+result[i]['Name']+"  "+result[i]['SRN']+"  "+result[i]['Section'],flush=True)
    channel.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming message from queue
channel.basic_consume(queue='read_database', on_message_callback=callback)

# Start consuming messages
channel.start_consuming()
