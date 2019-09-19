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

als_thread = MyThread(3, als, 12, 0)
bls_thread = MyThread(3, bls, 12, 0)

als_thread.start()
bls_thread.start()
