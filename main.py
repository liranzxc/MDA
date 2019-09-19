#!/usr/bin/env python
from publisherP.threadsPatient import PatientThread
import pika
import sys
import json
import time
from TreatmentsArea.TreamentConsumer import *
from publisherA.ThreadsAmbulance import MyThread
from threading import Thread

from EvacuationArea.EvacuationMain import Evan

from EvacuationArea.inAmbulance import *
from EvacuationArea.inPatient import *


timer = 0

def read_value():
    global timer
    return timer

def increment_time():
    global timer
    while True:
        time.sleep(1)
        print("Value before incrementing: " + str(timer))
        timer +=1


def thread_function(ambulances,u_p,non_u_p,dead_p):
    global timer
    currentTime = timer
    while True:
        time.sleep(1) # each 1 min  make des
        Evan.random_evacuation({},ambulances,u_p,non_u_p,dead_p,currentTime)

if __name__ == "__main__":
    incr_thread = threading.Thread(target=increment_time)
    incr_thread.start()

    als = {
        "id": "generate later",
        "type": "ALS",
        "tZero": 0,
        "tCurrent": 0,
        "timeOut": 100000
    }

    bls = {
        "id": "generate later",
        "type": "BLS",
        "tZero": 0,
        "tCurrent": 0,
        "timeOut": 100000
    }

    initial_time = 0
    max_als = 12
    max_bls = 12
    refresh_time_als = 3
    refresh_time_bls = 3

    als_thread = MyThread(refresh_time_als, als, max_als, initial_time)
    bls_thread = MyThread(refresh_time_bls, bls, max_bls, initial_time)

    als_thread.start()
    bls_thread.start()

    #patient ganerator
    non_urgent = PatientThread(75, 0, 5, 15, 'n', 64, 100)
    urgent = PatientThread(45, 15, 15, 25, 'u', 15, 63)
    dead = PatientThread(30, 20, 10, 20, 'd', 0, 14)

    # star threads
    non_urgent.start()
    urgent.start()
    dead.start()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    connection2 = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channelAmbulans = connection2.channel()

    U_patients = []
    Non_U_patients = []
    DEAD_U_patients = []

    td = ThreamentWorker(U_patients, Non_U_patients, DEAD_U_patients, channel)
    td.setDaemon(False)
    td.start()

    ambulances = []

    U_patients_env = []
    Non_U_patients_env = []
    DEAD_U_patients_env = []

    ambulance_thread = Threaded_Ambulance(ambulances)
    patient_thread = Threaded_Patient(U_patients_env,Non_U_patients_env,DEAD_U_patients_env)

    ambulance_thread.start()
    patient_thread.start()
    #
    x = threading.Thread(target=thread_function,args=(ambulances,U_patients_env,Non_U_patients_env,DEAD_U_patients_env))
    x.start()


    TIME_DECISION = 5
    i = 0
    while True:
        time.sleep(TIME_DECISION)
        ModelCheck(U_patients, Non_U_patients, DEAD_U_patients, "TRIAGE-PRI", channelAmbulans)





