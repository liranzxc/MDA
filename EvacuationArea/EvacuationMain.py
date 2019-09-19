import threading

from inAmbulance import Threaded_Ambulance
from inPatient import Threaded_Patient

ambulance_thread = Threaded_Ambulance([])

patient_thread = Threaded_Patient([])

ambulance_thread.start()

patient_thread.start()