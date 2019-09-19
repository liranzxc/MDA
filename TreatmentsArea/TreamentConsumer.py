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
        print(body)
        if(body["type"] == 'u'):
            self.u_p.append(body)
        if (body["type"] == 'n'):
            self.non_u_p.append(body)
        if (body["type"] == 'd'):
            self.dead_p.append(body)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __init__(self, u_p,non_u_p,dead_p):
        threading.Thread.__init__(self)
        self.u_p = u_p
        self.non_u_p = non_u_p
        self.dead_p = dead_p
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='Patients_queue', durable=True)
        print(' [*] Waiting for patients. To exit press CTRL+C')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='Patients_queue', on_message_callback=self.callback)

    def run(self):
        print('start consuming')
        self.channel.start_consuming()



def ModelCheck(U_patients,Non_U_patients,DEAD_U_patients,Model):
    if(Model == 'Random'):




if __name__ == "__main__":
    U_patients = []
    Non_U_patients = []
    DEAD_U_patients = []

    td = ThreamentWorker(U_patients,Non_U_patients,DEAD_U_patients)
    td.setDaemon(False)
    td.start()

    TIME_DECISION = 1
    i = 0
    while True:
        print(U_patients)
        print(Non_U_patients)
        print(DEAD_U_patients)
        time.sleep(TIME_DECISION)



