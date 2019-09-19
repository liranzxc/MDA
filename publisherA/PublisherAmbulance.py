# !/usr/bin/env python
import pika
import sys
import json
import time


from ThreadsAmbulance import MyThread

als = {
    "id": "0",
    "type": "ALS",
    "tZero": 0,
    "tDelta": 0,
    "timeOut": 0
}

bls = {
    "id": "number",
    "type": "BLS",
    "tZero": 0,
    "tCurrent": 0,
    "timeOut": 0
}

als_thread = MyThread(3, als, 12, time.time())
bls_thread = MyThread(3, bls, 12, time.time())

als_thread.start()
bls_thread.start()

als_thread.join()
bls_thread.join()
