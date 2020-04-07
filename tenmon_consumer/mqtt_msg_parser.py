import src.utils.paho.mqtt.client as mqtt
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv

PG_DATABASE = getenv('POSTGRES_DATABASE', 'postgres')
PG_HOSTNAME = getenv('POSTGRES_HOSTNAME', 'localhost')
PG_PORT = getenv('POSTGRES_PORT', '5432')
PG_USERNAME = getenv('POSTGRES_USER', 'postgres')
PG_PASSWORD = getenv('POSTGRES_PASSWORD', 'k4km0nster')

# MQTT Settings
MQTT_Broker = getenv("MQTT_BROKER", 'localhost')
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "/mqtt/slb/gateway/#"
QOS = 1
DEBUG = True


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class Config:
    def __init__(self, dbo):
        self.dbo = dbo

    def get_conf_from_db(self):
        try:
            res = self.dbo.do_select("select topic, action from gateway_actions;", return_as_dict=True)
        except Exception as e:
            print("Exception in get_conf_from_db: {}".format(e))
            return e

        return res



@singleton
class DatabaseManager:
    """
    Postgres Database Manager class using psycopg2 controled by env
    POSTGRES_DATABASE
    POSTGRES_HOSTNAME
    POSTGRES_PORT
    POSTGRES_USER
    POSTGRES_PASSWORD
    """
    def __init__(self):
        self.conn = psycopg2.connect(host=PG_HOSTNAME, user=PG_USERNAME, password=PG_PASSWORD, dbname=PG_DATABASE)
        self.cur = self.conn.cursor()
        self.cur.execute("SET application_name TO 'MQTT to Postgres Gateway';")
        self.rctimer = time.time()

    def do_insert_update_delete(self, sql_query, args=()):
        print(sql_query)
        if (15 - ((time.time() - self.rctimer))) < 0:
            self.rctimer = time.time()
            try:
                self.cur.execute("select 1")
            except Exception as e1:
                if DEBUG:
                    print("reconnect now: " + e1)
                    self.conn = psycopg2.connect(host=PG_HOSTNAME, user=PG_USERNAME, password=PG_PASSWORD,
                                                 dbname=PG_DATABASE)

            # If the SQL statement fails for some reason, do a rollback. Otherwise we will hang with "idle in transaction(aborted)" which is bad, bad, bad. Patrik.

        try:
            self.cur.execute(sql_query, args)
        except Exception as e:
            self.conn.rollback()
        else:
            self.conn.commit()

        return None

    def do_select(self, sql_query, return_as_dict=False):

        try:
            self.cur.execute(sql_query)
            a = self.cur.fetchall()
        except Exception as e:
            print("Exception in do_select: {}".format(e))
            return e

        if return_as_dict:
            actions = dict((x, y) for x, y in a)  # Not Generic will fail if more than 2 columns
            return actions

        return a

    def __del__(self):
        self.cur.close()
        self.conn.close()


class Mqtt:
    def __init__(self, dbo, cnf):
        self.dbo = dbo
        self.config = cnf
        self.mqttc = mqtt.Client()

        # Assign event callbacks
        self.mqttc.on_message = self._on_message
        self.mqttc.on_connect = self._on_connect
        self.mqttc.on_subscribe = self._on_subscribe
        self.mqttc.on_disconnect = self._on_disconnect
        # self.mqttc.username_pw_set(username="postgres", password="k4km0nster")

        self.actions = self.config.get_conf_from_db()

    def Data_Handler(self, topic, payload, dbg=False):
        try:
            self.dbo.do_insert_update_delete(self.actions[topic] % (payload))
        except Exception, e:
            print("Exception In Data_Handler: {}".format(e))
            return e

        return True

    def _on_connect(self, mosq, obj, rc):
        print(self.mqttc.subscribe(MQTT_Topic, 0))

    # Save Data into DB Table
    def _on_message(self, mosq, obj, msg):
        if DEBUG:
            print(str(msg.topic), str(msg.payload.decode()))
        self.Data_Handler(str(msg.topic), str(msg.payload.decode()), DEBUG)

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        if DEBUG:
            print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0 and DEBUG:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    def start(self):

        # Connect to MQTT
        self.mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
        self.mqttc.subscribe(MQTT_Topic, QOS)

        # Continue the network loop
        self.mqttc.loop_forever()


if __name__ == "__main__":
    dbm = DatabaseManager()
    cnf = Config(dbm)

    Mqtt(dbm, cnf).start()