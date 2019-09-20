import threading, sys
import random, pika, operator

# from inAmbulance import Threaded_Ambulance
# from inPatient import Threaded_Patient
from EvacuationArea.ThreadAmbulanceBack import *


from EvacuationArea.ThreadAmbulanceBack import *
from TreatmentsArea.TreamentConsumer import *

# from TreatmentConsumer import UpdateProbability
#
# ambulances = []
# patients = []
# currentTime = 0
#
# ambulance_thread = Threaded_Ambulance(ambulances)
# patient_thread = Threaded_Patient(patients)
#
# ambulance_thread.start()
# patient_thread.start()
#
# while True:
#     time.sleep(1)
#     currentTime += 1
#     random_evacuation()
#     fifo()


class Evan:
    def random_evacuation(self,ambulances,u_p,non_u_p,dead_p,currentTime):
        patient = None
        if ambulances:
            ambulance = random.choice(ambulances)
            if ambulance['type'] == 'ALS':
                if u_p and dead_p:
                    patient = random.choice(u_p + dead_p)
                elif u_p:
                    patient = random.choice(u_p)
                elif dead_p:
                    patient = random.choice(dead_p)
            else:
                if non_u_p:
                    patient = random.choice(non_u_p)
                    # non_u_p[patient]['leave'] = currentTime

            if patient != None:
                ambulances.remove(ambulance)
                if (patient["type"] == 'u'):
                    u_p.remove(patient)
                if (patient["type"] == 'n'):
                    non_u_p.remove(patient)
                if (patient["type"] == 'd'):
                    dead_p.remove(patient)
               # print('patient: %r in ambulance %r left in time %r' % (patient, ambulance, currentTime))
                patient["LeftTime"] = currentTime

                print(patient)
                return_ambulance = ThreadAmbulanceBack(ambulance, currentTime)
                return_ambulance.start()
#                UpdateProbability(u_p, non_u_p, dead_p, 0)


    def fifo(self,ambulances,u_p,non_u_p,dead_p, currentTime):
        if ambulances:
            ambulance = ambulances[0]
            patient = None
            if ambulance['type'] is "ALS":
                if u_p:
                    patient = u_p[0]
            else:
                if non_u_p:
                    patient = non_u_p[0]

            if patient is not None:

                print("patient %r in ambulance %r left in time %r" %(patient, ambulance, currentTime))

                ambulances.remove(ambulance)

                if (patient["type"] == 'u'):
                    u_p.remove(patient)
                if (patient["type"] == 'n'):
                    non_u_p.remove(patient)

                return_ambulance = ThreadAmbulanceBack(ambulance, currentTime)
                return_ambulance.start()

        UpdateProbability(u_p, non_u_p, dead_p, 0.5)

    def urgent_fifo(self,ambulances,u_p,non_u_p,dead_p, currentTime):
        if ambulances:
            if u_p:
                for i in range(0, len(ambulances)):
                    ambulance = ambulances[i]
                    if ambulance['type'] is "ALS":
                        patient = u_p[0]
                        print("patient %r in ambulance %r left in time %r" % (patient, ambulance, currentTime))
                        ambulances.remove(ambulance)
                        u_p.remove(patient)
                        return_ambulance = ThreadAmbulanceBack(ambulance, currentTime)
                        return_ambulance.start()
                        UpdateProbability(u_p, non_u_p, dead_p, 1)


    def full_capacity(self,ambulances,u_p,non_u_p,dead_p, currentTime):
        if ambulances:
            if patients.empty:
                ambulances.sort(key=operator.itemgetter('type'))
                count = -1
                for i in patients:
                    count += 1
                    if patients[count]['in_ambulance'] is False:
                        for j in range(0, len(ambulances)):
                            if ambulances[j]['type'] is "ALS":
                                if patients[count]['type'] is "u":
                                    if len(ambulances[j]['u']) < 1:
                                        ambulances[j]['u'].append(patient)
                                        print("patient %r in ambulance %r left in time %r" % (patients[count],
                                                                                              ambulances[j], currentTime))
                                        patients[count]['in_ambulance'] = True
                                        break
                                    continue
                                if patients[count]['type'] is "n":
                                    if len(ambulances[j]['n']) < 2:
                                        ambulances[j]['n'].append(patient)
                                        print("patient %r in ambulance %r left in time %r" % (patients[count],
                                                                                              ambulances[j], currentTime))
                                        patients[count]['in_ambulance'] = True
                                        break
                                    continue
                            if ambulances[j]['type'] is "BLS":
                                if patients[count]['type'] is "n":
                                    if len(ambulances[j]['n']) < 3:
                                        ambulances[j]['n'].append(patient)
                                        print("patient %r in ambulance %r left in time %r" % (patients[count],
                                                                                              ambulances[j], currentTime))
                                        patients[count]['in_ambulance'] = True
                                        break
                                    continue
                send_ambulances = []
                for ambulance in ambulances:
                    if ambulance['type'] is 'ALS':
                        if len(ambulance['u']) == 1 and len(ambulance['n']) == 2:
                            send_ambulances.append(ambulance)
                            for i in range(0, len(ambulance['n'])):
                                patients.remove(ambulance['n'][i])
                            patients.remove(ambulance['u'][0])
                    else:
                        if len(ambulance['n']) == 3:
                            send_ambulances.append(ambulance)
                        for i in range(0, len(ambulance['n'])):
                            patients.remove(ambulance['n'][i])
                    ambulances.remove(ambulance)
                    return_ambulance = ThreadAmbulanceBack(ambulance, currentTime)
                    return_ambulance.start()
                    UpdateProbability(list(filter(lambda d: d['type'] is 'u', patients)),
                                      list(filter(lambda d: d['type'] is 'n', patients)),
                                      list(filter(lambda d: d['type'] is 'd', patients)),
                                      1)


    def triage(self,ambulances,u_p,non_u_p,dead_p, currentTime):
        if ambulances:
            if u_p:
                for patient in u_p:
                    als_ambulances = list(filter(lambda d: d['type'] is 'ALS', ambulances))
                    if len(als_ambulances) != 0:
                        print("patient %r in ambulance %r left in time %r" % (patient,
                                                                          als_ambulances[0], currentTime))
                    ambulances.remove(als_ambulances[0])
                    u_p.remove(patient)
                    return_ambulance = ThreadAmbulanceBack(als_ambulances[0], currentTime)
                    return_ambulance.start()
            elif non_u_p:
                for patient in non_u_p:
                        print("patient %r in ambulance %r left in time %r" % (patient,
                                                                              ambulances[0], currentTime))
                        ambulance = ambulances[0]
                        ambulances.remove(ambulance)
                        non_u_p.remove(patient)
                        return_ambulance = ThreadAmbulanceBack(ambulance, currentTime)
                        return_ambulance.start()
                        UpdateProbability(u_p, non_u_p, dead_p, 2)
