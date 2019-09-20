import threading, sys
import random, pika, operator

# from inAmbulance import Threaded_Ambulance
# from inPatient import Threaded_Patient
# from ThreadAmbulanceBack import ThreadAmbulanceBack
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
    def random_evacuation(self,ambulances,u_p,non_u_p,dead_p, currentTime):
        currentTime += 1
        if ambulances:
            ambulance = random.choice(ambulances)
            if ambulance['type'] == "ALS":
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

            # print("patient %r in ambulance %r left in time %r" %(patient, ambulance, currentTime))
            ambulances.remove(ambulance)
            try:
                non_u_p.remove(patient)
                u_p.remove(patient)
                dead_p.remove(patient)
            except:
                print("maybe not deleted")
            return_ambulance = ThreadAmbulanceBack(ambulance, currentTime)
            return_ambulance.start()
            UpdateProbability(u_p, non_u_p, dead_p, 0)


    def fifo(self,ambulances,u_p,non_u_p,dead_p, currentTime):
        ambulance = ambulances[0]
        if ambulance['type'] == "ALS":
            if u_p:
                patient = u_p[0]
        else:
            if non_u_p:
                patient = non_u_p[0]
        print("patient %r in ambulance %r left in time %r" %(patient, ambulance, currentTime))
        ambulances.remove(ambulance)
        try:
            non_u_p.remove(patient)
            u_p.remove(patient)
        except:
            print("maybe not deleted")
        return_ambulance = ThreadAmbulanceBack(ambulance, currentTime)
        return_ambulance.start()
        UpdateProbability(u_p, non_u_p, dead_p, 0.5)

    def urgent_fifo(self,ambulances,u_p,non_u_p,dead_p, currentTime):
        if ambulances:
            if u_p:
                for i in range(0, len(ambulances)):
                    ambulance = ambulances[i]
                    if ambulance['type'] == "ALS":
                        patient = u_p[0]
                        print("patient %r in ambulance %r left in time %r" % (patient, ambulance, currentTime))
                        ambulances.remove(ambulance)
                        u_p.remove(patient)
                        return_ambulance = ThreadAmbulanceBack(ambulance, currentTime)
                        return_ambulance.start()
                        UpdateProbability(u_p, non_u_p, dead_p, 1)


    def full_capacity(self,ambulances,u_p,non_u_p,dead_p, currentTime):
        if ambulances:
            ambulances.sort(key=operator.itemgetter('type'))
            for j in range(0, len(ambulances)):
                if ambulances[j]['type'] == "ALS":
                    if len(out_u_p = list(filter(lambda d: d['in_ambulance'] is False, u_p))) != 0:
                        if len(ambulances[j]['u']) < 1:
                            patient = out_u_p[0]
                            ambulances[j]['u'].append(patient)
                            print("patient %r in ambulance %r left in time %r" % (patient,
                                                                                  ambulances[j], currentTime))
                            i = u_p.index(patient)
                            u_p[i]['in_ambulance'] = True
                            break
                        continue
                    if len(out_non_u_p = list(filter(lambda d: d['in_ambulance'] is False, non_u_p))) != 0:
                        if len(ambulances[j]['n']) < 2:
                            patient = out_non_u_p[0]
                            ambulances[j]['n'].append(patient)
                            print("patient %r in ambulance %r left in time %r" % (patient,
                                                                                  ambulances[j], currentTime))
                            i = non_u_p.index(patient)
                            non_u_p[i]['in_ambulance'] = True
                            break
                        continue
                if ambulances[j]['type'] == "BLS":
                    if len(out_non_u_p = list(filter(lambda d: d['in_ambulance'] is False, non_u_p))) != 0:
                        if len(ambulances[j]['n']) < 3:
                            patient = out_non_u_p[0]
                            ambulances[j]['n'].append(patient)
                            print("patient %r in ambulance %r left in time %r" % (patient,
                                                                                  ambulances[j], currentTime))
                            i = non_u_p.index(patient)
                            non_u_p[i]['in_ambulance'] = True
                            break
                        continue
            send_ambulances = []
            for ambulance in ambulances:
                if ambulance['type'] == 'ALS':
                    if len(ambulance['u']) == 1 and len(ambulance['n']) == 2:
                        send_ambulances.append(ambulance)
                        for i in range(0, len(ambulance['n'])):
                            non_u_p.remove(ambulance['n'][i])
                        u_p.remove(ambulance['u'][0])
                else:
                    if len(ambulance['n']) == 3:
                        send_ambulances.append(ambulance)
                    for i in range(0, len(ambulance['n'])):
                        non_u_p.remove(ambulance['n'][i])
                ambulances.remove(ambulance)
                return_ambulance = ThreadAmbulanceBack(ambulance, currentTime)
                return_ambulance.start()
        UpdateProbability(u_p, non_u_p, dead_p, 1)


    def triage(self,ambulances,u_p,non_u_p,dead_p, currentTime):
        if ambulances:
            if u_p:
                patient = u_p[0]
                als_ambulances = list(filter(lambda d: d['type'] == 'ALS', ambulances))
                if len(als_ambulances) != 0:
                    print("patient %r in ambulance %r left in time %r" % (patient,
                                                                      als_ambulances[0], currentTime))
                ambulances.remove(als_ambulances[0])
                u_p.remove(patient)
                return_ambulance = ThreadAmbulanceBack(als_ambulances[0], currentTime)
                return_ambulance.start()
            elif non_u_p:
                patient = non_u_p[0]
                print("patient %r in ambulance %r left in time %r" % (patient,
                                                                      ambulances[0], currentTime))
                ambulance = ambulances[0]
                ambulances.remove(ambulance)
                non_u_p.remove(patient)
                return_ambulance = ThreadAmbulanceBack(ambulance, currentTime)
                return_ambulance.start()
        UpdateProbability(u_p, non_u_p, dead_p, 2)
