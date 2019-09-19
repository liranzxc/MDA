#!/usr/bin/env python
import pika
import sys
import json
import random

CURRENT_TIME = 0

def publish_patient(patient):
    channel.basic_publish(
        exchange='',
        routing_key='Patients_queue',
        body=patient,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

def make_patient(max, t_zero, ran_from, ran_to, patient_type):
    counter = 1
    sleep(t_zero)
    cur_time = t_zero
    while counter <= max:
        time_to_send = (random.randint(ran_from, ran_to) / 10)
        sleep(time_to_send)
        cur_time = cur_time + time_to_send
        patient = {
          "id" : counter ,
          "type"  : patient_type,
          "tZero" : t_zero,
          'probability' : 0.9 ,
          "cur_time" : cur_time ,
        }
        print(json.dumps(patient))
        # publish_patient(json.dumps(patient))
        counter += 1

if __name__ == "__main__":
    #start rabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.43.136'))
    channel = connection.channel()
    channel.queue_declare(queue='Patients_queue', durable=True)
    message = ' '.join(sys.argv[1:]) or "Hello liran World!"

    #star threads

    #change current time by 0.1 min
    while True:
        CURRENT_TIME +=0.1
        sleep(0.1)

    connection.close()

