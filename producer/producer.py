import pika,json
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def routes():
    message = {
        "to health check": "http://localhost:5050/health_check",
        "to insert data": "http://localhost:5050/insert_record",
        "to read data": "http://localhost:5050/read_database",
        "to delete data": "http://localhost:5050/delete_record"
    }
    
    return json.dumps(message, indent = 4)

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# RabbitMQ exchange and queue names
exchange_name = 'my_exchange'
health_check_queue = 'health_check'
insert_record_queue = 'insert_record'
read_database_queue = 'read_database'
delete_record_queue = 'delete_record'

# Declare exchange and queues
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

channel.queue_declare(queue=health_check_queue)
channel.queue_bind(exchange=exchange_name, queue=health_check_queue, routing_key=health_check_queue)

channel.queue_declare(queue=insert_record_queue)
channel.queue_bind(exchange=exchange_name, queue=insert_record_queue, routing_key=insert_record_queue)

channel.queue_declare(queue=read_database_queue)
channel.queue_bind(exchange=exchange_name, queue=read_database_queue, routing_key=read_database_queue)

channel.queue_declare(queue=delete_record_queue)
channel.queue_bind(exchange=exchange_name, queue=delete_record_queue, routing_key=delete_record_queue)

# HTTP route to send health-check message to health_check_queue
@app.route('/health_check', methods=['GET'])
def health_check():
    health_check_message = request.args.get('check', default='', type=str)
    channel.basic_publish(exchange=exchange_name, routing_key=health_check_queue, body=health_check_message)
    return 'Health check message sent to health_check Queue.'

# HTTP route to send insert-record message to insert_record_queue
@app.route('/insert_record', methods=['POST'])
def insert_record():
    record = request.get_json()
    name = record.get('Name')
    srn = record.get('SRN')
    section = record.get('Section')
    body = f'{{"Name":"{name}","SRN":"{srn}","Section":"{section}"}}'
    channel.basic_publish(exchange=exchange_name, routing_key=insert_record_queue, body=body)
    return 'Insert record message sent to insert_record Queue.'

# HTTP route to send read-database message to read_database_queue
@app.route('/read_database', methods=['GET'])
def read_database():
    channel.basic_publish(exchange=exchange_name, routing_key=read_database_queue, body='')
    return 'Read database message sent to read_database Queue.'

# HTTP route to send delete-record message to delete_record_queue
@app.route('/delete_record', methods=['GET'])
def delete_record():
    srn = request.args.get('SRN', default='', type=str)
    channel.basic_publish(exchange=exchange_name, routing_key=delete_record_queue, body=srn)
    return f'Delete record message sent to delete_record Queue for SRN: {srn}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

