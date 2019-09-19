from threading import Thread
import pika
import json
import time


class MyThread(Thread):
    def __init__(self, refresh_time, ambulance, max_ambulances):
        ''' Constructor. '''

        Thread.__init__(self)
        self.refresh_time = refresh_time
        self.ambulance = ambulance
        self.max_ambulances = max_ambulances
        self.current_ambulances = 0

    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.43.136'))
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)

        while self.current_ambulances < self.max_ambulances:
            channel.basic_publish(
                exchange='',
                routing_key='Ambulance_queue',
                body=json.dumps(self.ambulance),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ))
            self.current_ambulances += 1
            time.sleep(self.refresh_time)
