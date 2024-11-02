import pika
import json

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    return connection, channel

def send_email_message(queue, message):
    connection, channel = get_rabbitmq_connection()

    channel.queue_declare(queue='queue', durable=True)
    message = json.dumps(message)
    # Set delivery properties with persistent delivery mode
    properties = pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
    
    channel.basic_publish(exchange='', routing_key=queue, body=message, properties=properties)
    connection.close()

def send_log_message(message):
    connection, channel = get_rabbitmq_connection()
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    
    message = json.dumps(message)
    
    # Set delivery properties with persistent delivery mode
    properties = pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)

    channel.basic_publish(exchange='logs', routing_key='', body=message, properties=properties)
    connection.close()