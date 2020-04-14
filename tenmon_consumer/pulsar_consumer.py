import pulsar
import time

client = pulsar.Client('pulsar://127.0.0.1:6650')

consumer = client.subscribe('my-topic', 'apan')
consumer2 = client.subscribe('persistent://tenforward/clients/register', 'apan')

while True:
    msg = consumer2.receive()

    try:
        print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
        # Acknowledge successful processing of the message
        print(consumer.acknowledge_cumulative(msg))
    except:
        # Message failed to be processed
        consumer.negative_acknowledge(msg)

client.close()