import threading, sys
import random, pika

from inAmbulance import Threaded_Ambulance
from inPatient import Threaded_Patient

ambulances = []
patients = []
currentTime = 0

ambulance_thread = Threaded_Ambulance(ambulances)
patient_thread = Threaded_Patient(patients)

ambulance_thread.start()
patient_thread.start()

while True:
    time.sleep(1)
    currentTime += 1
    randomEvac()


def randomEvac():

    ambulance = random.choice(ambulances)
    patient = random.choice(patients)
    print("patient %r in ambulance %r" %(patient, ambulance))
    ambulances.remove(ambulance)
    patients.remove(patient)
    returnAmbulance()

def returnAmbulance():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.43.136'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    message = ' '.join(sys.argv[1:]) or "Hello liran World!"

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent %r" % message)
    connection.close()
