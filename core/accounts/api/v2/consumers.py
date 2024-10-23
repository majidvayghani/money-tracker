import sys
import os

# Get the current directory and add the parent directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

# Set the default Django settings module for the 'core' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

import django
django.setup()

"""
i don’t know why I have to do the above configuration

"""

from rabbitmq import get_rabbitmq_connection
from django.core.mail import send_mail
from core.settings.base import *
import json

def process_signup_message(message):
    email = message.get('email')
    
    send_email(email)

def send_email(to_email):
    subject = "Welcome to Our Service"
    message = f"Hi {to_email}, \n This message is sent with RabbitMQ.!"
    from_email = DEFAULT_FROM_EMAIL
 
    send_mail(subject, message, from_email, [to_email])

def consume_message(queue, callback):
    connection, channel = get_rabbitmq_connection()
    channel.queue_declare(queue=queue, durable=True)

    def on_message(ch, method, properties, body):
        callback(json.loads(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=on_message)
    print(f" [*] Waiting for messages in queue '{queue}'. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_message('signup_queue', process_signup_message)