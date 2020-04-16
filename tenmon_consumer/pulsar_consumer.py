import pulsar
import threading
import time, sys
from utils import jwt
import psycopg2

clientname = "Tenmon Pulsar to PostgreSQL parser"
client = pulsar.Client('pulsar://127.0.0.1:6650')
topics_to_proccess = ['non-persistent://tenforward/clients/register', 'persistent://tenforward/clients/config']

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class DatabaseManager:

    def __init__(self):
        self.conn = psycopg2.connect(host='127.0.0.1', user='postgres',
                                     password='0oBSTinatenEss#maRyl7uMbeL0@3162',
                                     dbname='postgres')
        self.cur = self.conn.cursor()
        self.cur.execute("SET application_name TO '{}';".format(clientname))
        self.rctimer = time.time()

    def do_insert_update_delete(self, sql_query, args=()):
        print(sql_query)
        # If the SQL statement fails for some reason, do a rollback. Otherwise we will hang with "idle in transaction(aborted)" which is bad, bad, bad. Patrik.
        try:
            self.cur.execute(sql_query, args)
        except Exception, e:
            self.conn.rollback()
        else:
            self.conn.commit()
        return None

    def _do_select(self, sql_query):
        try:
            self.cur.execute(sql_query)
            a = self.cur.fetchone()
        except Exception, e:
            print("Exception in do_select: {}".format(e))
            return e
        return a

    def get_uniquekey(self, customerid):
        """Run a SQL query to select rows from table."""
        cid = self._do_select("""SELECT uniquekey FROM public.customers WHERE customerid = '{}'""".format(customerid))
        return cid[0]

    def __del__(self):
        self.cur.close()
        self.conn.close()


class Register:
    def __init__(self, header, token):
        self.customerid = header.get('customerid')

        self.db = DatabaseManager()

        self.token = token
        self.uniquekey = self._getuniquekey()

        self.client = None

    def _getuniquekey(self):
        return self.db.get_uniquekey(self.customerid)

    def verify_token(self):
        try:
            self.client = jwt.decode(self.token, self.uniquekey, algorithms='HS512')
            # Message failed to be processed
            print(self.client)
            return "True"
        except:
            print("Signature missmatch2")
            return "False"




def process_topic(tpcs=None):
    print(tpcs)
    consumer = client.subscribe(tpcs, clientname)
    while True:
        msg = consumer.receive()
        try:
            token = msg.data()
            header = jwt.get_unverified_header(token)
            # print(jwt.decode(token, verify=False))
            print(Register(header, token).verify_token())
            #print("Received message '{}' id='{}'".format(token, msg.message_id()))
            # Acknowledge successful processing of the message
            consumer.acknowledge_cumulative(msg)
        except:
            # Message failed to be processed
            print("Signature missmatch")
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

