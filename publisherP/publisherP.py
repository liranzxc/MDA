#!/usr/bin/env python
import sys
from threadsPatient import PatientThread

if __name__ == "__main__":
    #star threads
    non_urgent = PatientThread(75, 0, 5, 15, 'n',0.9)
    urgent = PatientThread(45, 15, 15, 25, 'u',0.5)
    dead = PatientThread(30, 20, 10, 20, 'd',0)


    non_urgent.start()
    urgent.start()
    dead.start()
