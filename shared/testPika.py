#!/usr/bin/env python
import pika
import time, threading


class Threaded_worker(threading.Thread):
    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        print("append to message array")
        self.messages.append(body)
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __init__(self, messages):
        threading.Thread.__init__(self)
        self.messages = messages
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(
            
            queue='Patients_queue', durable=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='Patients_queue', on_message_callback=self.callback)

    def run(self):
        print('start consuming')
        self.channel.start_consuming()


if __name__ == "__main__":
    messages = []
    td = Threaded_worker(messages)
    td.setDaemon(False)
    td.start()
    i = 0
    while i < 1000000:
        print("here")
        print(messages)
        time.sleep(0.1)
        i += 1
