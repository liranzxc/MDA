from threading import Thread
import uuid
import pika
import json
import random
from time import sleep

class PatientThread(Thread):

    def __init__(self, max_patient, t_zero, ran_from, ran_to, patient_type, probability_from, probability_to):
        ''' Constructor. '''
        Thread.__init__(self)
        self.max_patient = max_patient
        self.t_zero = t_zero
        self.ran_from = ran_from #random from number
        self.ran_to = ran_to #random to number
        self.patient_type = patient_type
        self.current_patients = 0
        self.patient = {
            'id' : 0 ,
            'type'  : '',
            'tZero' : 0,
            'probability' : 0 ,
            'cur_time' : 0 ,
            "in_ambulance": False,
        }
        self.probability_from = probability_from #for random probability
        self.probability_to = probability_to #for random probability
        self.current_time = t_zero
        self.channel = ''

    def publish_patient(self, patient, ):
        self.channel.basic_publish(
            exchange='',
            routing_key='Patients_queue',
            body=patient,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

    def run(self):
        # start rabbitMQ Connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.43.136'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='Patients_queue', durable=True)

        #sleep until the time to start send
        sleep(self.t_zero)
        #sending patient to queue
        while self.current_patients < self.max_patient:
            # Changing patient Details
            self.patient['id'] = str(uuid.uuid1())
            self.patient['type'] = self.patient_type
            self.patient['tZero'] = 0
            self.patient['probability'] = random.randint(self.probability_from, self.probability_to)
            time_to_send = (random.randint(self.ran_from, self.ran_to) / 10)
            sleep(time_to_send)
            self.current_time = self.current_time + time_to_send
            self.patient['cur_time'] = self.current_time
            self.publish_patient(json.dumps(self.patient))
            #print(json.dumps(self.patient))
            self.current_patients += 1
        connection.close()
