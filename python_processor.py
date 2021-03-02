#!/usr/bin/env python

import os
import sys
import pika

from util.http_status_server import HttpHealthServer
from util.task_args import get_rabbitmq_binder, get_input_queue, get_output_queue, get_reverse_string, get_rabbitmq_binder_username, get_rabbitmq_binder_password

credentials = pika.PlainCredentials(get_rabbitmq_binder_username(), get_rabbitmq_binder_password())
parameters = pika.ConnectionParameters(credentials=credentials)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=get_rabbitmq_binder(),credentials=credentials))
inputQueue = connection.channel()
inputQueue.queue_declare(queue=get_input_queue(),durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    reverse_string = get_reverse_string()
    output_message = body.decode()
    if reverse_string is not None and reverse_string.lower() == "true":
        output_message = "".join(reversed(output_message))

    outputQueue = connection.channel()
    outputQueue.queue_declare(queue=get_output_queue(),durable=True)
    outputQueue.basic_publish(exchange='', routing_key=get_output_queue(), body=output_message)
    print(" [x] Sent %r" % output_message)

HttpHealthServer.run_thread()

inputQueue.basic_qos(prefetch_count=1)
inputQueue.basic_consume(queue=get_input_queue(), on_message_callback=callback, auto_ack=True)
inputQueue.start_consuming()
print(' [*] Waiting for messages. To exit press CTRL+C')