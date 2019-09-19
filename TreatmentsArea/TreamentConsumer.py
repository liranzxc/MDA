#!/usr/bin/env python
import pika
import time, threading
import json
import random

class ThreamentWorker(threading.Thread):
    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        print("append to message array")
        body = json.loads(body.decode('utf-8')) # decode json
        if(body["type"] == 'u'):
            self.u_p.append(body)
        if (body["type"] == 'n'):
            self.non_u_p.append(body)
        if (body["type"] == 'd'):
            self.dead_p.append(body)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __init__(self, u_p,non_u_p,dead_p,channel):
        threading.Thread.__init__(self)
        self.u_p = u_p
        self.non_u_p = non_u_p
        self.dead_p = dead_p
        self.channel = channel
        self.channel.queue_declare(queue='Patients_queue', durable=True)
        print(' [*] Waiting for patients. To exit press CTRL+C')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='Patients_queue', on_message_callback=self.callback)

    def run(self):
        print('start consuming')
        self.channel.start_consuming()



def ModelCheck(U_patients,Non_U_patients,DEAD_U_patients,Model,channel):
    print("check model")

    selected = {}
    if(Model == 'RANDOM'):
        patients = []
        if(len(U_patients) > 0):
            patients += (U_patients)
        if(len(Non_U_patients) > 0):
            patients += (Non_U_patients)
        if(len(DEAD_U_patients) > 0):
            patients += (DEAD_U_patients)

        if(len(patients) > 0):
            selected = random.choice(patients)
            print("selectend",selected)

            if (selected["type"] == 'u'):
                U_patients.remove(selected)
            if (selected["type"] == 'n'):
                Non_U_patients.remove(selected)
            if (selected["type"] == 'd'):
                DEAD_U_patients.remove(selected)
        else:
            print("not patients")
    elif Model == "FIFO":
        patients = []
        if (len(U_patients) > 0):
            patients += (U_patients[0])
        if (len(Non_U_patients) > 0):
            patients += (Non_U_patients[0])
        if (len(DEAD_U_patients) > 0):
            patients += (DEAD_U_patients[0])

        if (len(patients) > 0):
            selected = random.choice(patients)
            print("selectend", selected)

            if (selected["type"] == 'u'):
                U_patients.remove(selected)
            if (selected["type"] == 'n'):
                Non_U_patients.remove(selected)
            if (selected["type"] == 'd'):
                DEAD_U_patients.remove(selected)
        else:
            print("not patients")
    elif Model == "URGENT-FIFO":
        if (len(U_patients) > 0):
            selected = U_patients[0]
            U_patients.remove(selected)

        if (len(Non_U_patients) > 0):
            selected = Non_U_patients[0]
            Non_U_patients.remove(selected)

        if (len(DEAD_U_patients) > 0):
            selected = DEAD_U_patients[0]
            DEAD_U_patients.remove(selected)

    elif Model == "FULL-CAPACITY":

        U_patients_Min = { probability : 1.0}
        Non_U_patients_Min = { probability : 1.0}

        if (len(U_patients) > 0 ):
            U_patients_Min = min(U_patients, key=lambda x: x['probability'])
        if(len(Non_U_patients) > 0 ):
            Non_U_patients_Min = min(Non_U_patients, key=lambda x: x['probability'])

        if(U_patients_Min < Non_U_patients_Min):
            selected = U_patients_Min
            U_patients.remove(selected)
        else:
            selected = Non_U_patients_Min
            Non_U_patients.remove(selected)

        if(selected["probability"] == 1.0):
            selected == {}

    if(selected != {}):
        channel.queue_declare(queue='Patients_need_evac_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='Patients_need_evac_queue',
            body=json.dumps(selected),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        print(" [x] Sent %r" % selected)


if __name__ == "__main__":
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    connection2 = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channelAmbulans = connection2.channel()

    U_patients = []
    Non_U_patients = []
    DEAD_U_patients = []

    td = ThreamentWorker(U_patients,Non_U_patients,DEAD_U_patients,channel)
    td.setDaemon(False)
    td.start()

    TIME_DECISION = 5
    i = 0
    while True:
        # print(U_patients)
        # print(Non_U_patients)
        # print(DEAD_U_patients)
        time.sleep(TIME_DECISION)
        ModelCheck(U_patients,Non_U_patients,DEAD_U_patients,"URGENT-FIFO",channelAmbulans)


