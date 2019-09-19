from threading import Thread
import pika
import json
from time import sleep


class ThreadAmbulanceBack(Thread):

    def __init__(self, ambulance, current_time):
        ''' Constructor. '''
        Thread.__init__(self)
        self.ambulance = json.loads(ambulance.decode('utf-8'))
        self.current_time = current_time
        self.channel = ''

    def publish_ambulance(self, ambulance):
        self.channel.basic_publish(
            exchange='',
            routing_key='Ambulance_queue',
            body=ambulance,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

    def run(self):
        # start rabbitMQ Connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.43.136'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='Ambulance_queue', durable=True)

        #wiat until the ambulance come back
        sleep(10)
        #sending ambulance to queue
        self.current_time += 10
        self.ambulance['tCurrent'] = self.current_time
        self.publish_patient(json.dumps(self.ambulance))

        connection.close()
