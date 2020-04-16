import pulsar
import threading
import time
from utils import jwt
import psycopg2

clientname = "Tenmon Pulsar to PostgreSQL parser"
client = pulsar.Client('pulsar://127.0.0.1:6650')
topics_to_proccess = ['non-persistent://tenforward/clients/register', 'persistent://tenforward/clients/config']


def process_topic(tpcs=None):
    print(tpcs)
    consumer = client.subscribe(tpcs, clientname)
    while True:
        msg = consumer.receive()
        try:
            token = msg.data()
            print(jwt.get_unverified_header(token))
            #print("Received message '{}' id='{}'".format(token, msg.message_id()))
            data = jwt.decode(token, 'aV3ryS3cr3tPassw0rd', algorithms='HS512')
            # Acknowledge successful processing of the message
            print(data)
            consumer.acknowledge_cumulative(msg)
        except:
            # Message failed to be processed
            consumer.negative_acknowledge(msg)


if __name__ == '__main__':
    threads = []
    for topic in topics_to_proccess:
        t = threading.Thread(target=process_topic, kwargs=({'tpcs': topic}))
        t.start()
        threads.append(t)

    print(threads)
    while True:
        time.sleep(1)

