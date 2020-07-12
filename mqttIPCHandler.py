#!/usr/bin/python3
import time
import paho.mqtt.client as mqtt
import json
from logger import Logger

class MqttIPC(object):
    mqtt_broker_priv = "127.0.0.1"
    mqtt_port = 1883
    mqtt_keep_alive = 60

    CLIENT_ID = "multivac_feedback"

    #Topics
    MQTT_TOPIC_DATA = "multivac/feedback"   #Topic for commands send/recv

    #Connection Flag
    connected = False

    def __init__(self):
        self.Log = Logger("MqttIPC")
        self.Log.log("INIT")

        self.client = mqtt.Client(self.CLIENT_ID) #Creates unique ID

        # Register callbacks
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.Log.log("Connecting to broker at {}".format(self.mqtt_broker_priv))
        self.client.connect(self.mqtt_broker_priv, self.mqtt_port, self.mqtt_keep_alive)

    def start(self):
        self.client.loop_start() # Start message monitor thread

    def subscribe(self, topic=""):
        self.Log.log("Subscribe to {}".format(topic))
        self.client.subscribe(topic)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        self.Log.log("Connection returned {}".format(rc))
        self.subscribe(self.MQTT_TOPIC_DATA)
        self.connected = True

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        self.Log.log("Client disconected - {}".format(rc))

    def add_message_callback(self, func):
        self.on_message_callback = func

    def on_message(self, client, userdata, message):
        self.Log.log("Message Received: {} | On Topic: {}".format(message.payload.decode("utf-8"), message.topic))
        if(self.on_message_callback):
            self.Log.log("Calling on_message_callback")
            self.on_message_callback(client, userdata, message)
        else:
            self.Log.log("No message callback!")

    def is_connected(self):
        return self.connected

if __name__ == '__main__':
    mqtt = MqttIPC()
    mqtt.start()
    while 1:
        time.sleep(1)
