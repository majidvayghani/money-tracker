import pika
import json

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    return connection, channel

def send_message(queue, message):
    connection, channel = get_rabbitmq_connection()

    channel.queue_declare(queue='queue', durable=True)
    message = json.dumps(message)
    channel.basic_publish(exchange='', routing_key=queue, body=message,
                          delivery_mode = pika.DeliveryMode.Persistent)

    connection.close()

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