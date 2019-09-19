#!/usr/bin/env python
import sys
from threadsPatient import PatientThread

if __name__ == "__main__":
    non_urgent = PatientThread(75, 0, 5, 15, 'n', [0.84, 0.9, 0.94, 0.97, 0.98])
    urgent = PatientThread(45, 15, 15, 25, 'u', [0.15, 0.23, 0.35, 0.63])
    dead = PatientThread(30, 20, 10, 20, 'd', [0])

    #star threads
    non_urgent.start()
    urgent.start()
    dead.start()
