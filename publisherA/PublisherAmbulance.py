# !/usr/bin/env python
import pika
import sys
import json
import time


from ThreadsAmbulance import MyThread

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
