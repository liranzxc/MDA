# !/usr/bin/env python
import pika
import sys
import json
import time

from PublisherA.ThreadsAmbulance import run

als = {
    "id": "0",
    "type": "ALS",
    "tZero": 0,
    "tDelta": 0,
    "timeOut": 0
}

bls = {
    "id": "number",
    "type": "ALS",
    "tZero": 0,
    "tDelta": 0,
    "timeOut": 0
}

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.43.136'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


als_thread = MyThread(1, als, 12)
bls_thread = MyThread(1, als, 12)

# print(" [x] Sent %r" % message)
connection.close()
