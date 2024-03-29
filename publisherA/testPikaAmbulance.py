#!/usr/bin/env python
import pika
import time, threading
import json

class Threaded_worker(threading.Thread):
    def callback(self, ch, method, properties, body):
        body = json.loads(body.decode('utf-8'))
        print(" [x] Received %r" % body)
        print("append to message array")
        self.messages.append(body)
        time.sleep(5)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __init__(self, messages):
        threading.Thread.__init__(self)
        self.messages = messages
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.43.136'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='Ambulance_queue', durable=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='Ambulance_queue', on_message_callback=self.callback)

    def run(self):
        print('start consuming')
        self.channel.start_consuming()


if __name__ == "__main__":
    messages = []
    td = Threaded_worker(messages)
    td.setDaemon(False)
    td.start()
    i = 0
    while i < 100000:
        print("here")
        time.sleep(5)
        print(messages)
        i += 1
