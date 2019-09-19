#!/usr/bin/env python
import pika
import sys
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='Patients_queue', durable=True)

message = {}
message["type"] = "u"

channel.basic_publish(
    exchange='',
    routing_key='Patients_queue',
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
print(" [x] Sent %r" % message)
connection.close()