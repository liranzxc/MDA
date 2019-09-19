#!/usr/bin/env python
import sys
from threadsPatient import PatientThread

if __name__ == "__main__":
    non_urgent = PatientThread(75, 0, 5, 15, 'n', 64, 100)
    urgent = PatientThread(45, 15, 15, 25, 'u', 15, 63)
    dead = PatientThread(30, 20, 10, 20, 'd', 0, 14)

    #star threads
    non_urgent.start()
    urgent.start()
    dead.start()
