import pika
import time, threading
import json

#in patience

class Threaded_Patient(threading.Thread):
    def callback(self, ch, method, properties, body):
        body = json.loads(body.decode('utf-8')) # decode json
        print(" [x] Received %r" % body)
        print("append to message array")
        if (body["type"] == 'u'):
            self.u_p.append(body)
        if (body["type"] == 'n'):
            self.non_u_p.append(body)
        if (body["type"] == 'd'):
            self.dead_p.append(body)

        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __init__(self, u_p,non_u_p ,dead_p):
        threading.Thread.__init__(self)
        self.u_p = u_p
        self.non_u_p = non_u_p
        self.dead_p = dead_p

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.43.136'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='Patients_queue', durable=True)
        print(' [*] Waiting for patients. To exit press CTRL+C')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='Patients_queue', on_message_callback=self.callback)

    def run(self):
        print('start consuming')
        while True:
            self.channel.start_consuming()
            time.sleep(1)
#
#
# if __name__ == "__main__":
#     messages = []
#     td = Threaded_Patient(messages)
#     td.setDaemon(False)
#     td.start()
#     i = 0
#     while i < 1000000:
#         print("here")
#         print(messages)
#         time.sleep(0.5)
#         i += 1
