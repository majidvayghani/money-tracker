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

from rabbitmq import consume_message
from django.core.mail import send_mail
from core.settings.base import *

def process_signup_message(message):
    email = message.get('email')
    
    send_email(email)

def send_email(to_email):
    subject = "Welcome to Our Service"
    message = f"Hi {to_email}, \n This message is sent with RabbitMQ.!"
    from_email = DEFAULT_FROM_EMAIL
 
    send_mail(subject, message, from_email, [to_email])

if __name__ == '__main__':
    consume_message('signup_queue', process_signup_message)
