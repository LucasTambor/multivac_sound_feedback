import time
import json

from logger import Logger
from sound import Sound
class SoundHandle(object):
    MAX_DISTANCE = 300  #cm
    MIN_DISTANCE = 15   #cm

    def __init__(self, ipc):
        self.ipc = ipc
        self.Log = Logger("SoundHandler")
        self.sound = Sound()

        #add callback to ipc handler
        self.ipc.add_message_callback(self.on_message)
        self.ipc.start()

    def on_message(self, client, userdata, message):
        self.Log.log("Message Arrived")
        msgRecv = message.payload.decode("utf-8")
        try:
            dataRecv = json.loads(msgRecv)
            self.Log.log(dataRecv)
            self.handleMessage(dataRecv)
        except Exception as e:
            self.Log.log("Failed to parse message: {}".format(e))

    def handleMessage(self, data):
        if data['status'] is not None:
            self.handleStatus(data['status'])
            if not data['status']:
                return
        if data['horizontal'] is not None:
            self.handlePan(data['horizontal'])
        if data['vertical'] is not None:
            self.handleTone(data['vertical'])
        if data['distance'] is not None:
            self.handleDistance(data['distance'])

    def handleStatus(self, status):
        self.Log.log("STATUS: {}".format(status))
        if status == 0:
            self.sound.setStatus(False)
        elif status == 1:
            self.sound.setStatus(True)
        else:
            self.Log.log("Invalid Status")

    def handlePan(self, side):
        self.Log.log("PAN: {}".format(side))
        if side == "left":
            self.sound.setPan(self.sound.CHANNEL_LEFT)
        elif side == "right":
            self.sound.setPan(self.sound.CHANNEL_RIGHT)
        elif side == "center":
            self.sound.setPan(self.sound.CHANNEL_CENTER)
        else:
            self.Log.log("Invalid Pan")

    def handleTone(self, side):
        self.Log.log("PAN: {}".format(side))
        if side == "up":
            self.sound.setTone(self.sound.TONE_UP)
        elif side == "down":
            self.sound.setTone(self.sound.TONE_DOWN)
        elif side == "center":
            self.sound.setTone(self.sound.TONE_CENTER)
        else:
            self.Log.log("Invalid Pan")

    def handleDistance(self, distance):
        if distance > self.MAX_DISTANCE or distance < self.MIN_DISTANCE:
            self.Log.log("Invalid Distance")
            return
        newInterval = self.mapDistanceToInterval(distance)
        self.Log.log("INTERVAL: {}".format(newInterval))
        self.sound.setInterval(newInterval)

    def mapDistanceToInterval(self, distance):
        return (distance - self.MIN_DISTANCE) * (self.sound.MAX_INTERVAL - self.sound.MIN_INTERVAL) / (self.MAX_DISTANCE - self.MIN_DISTANCE) + self.sound.MIN_INTERVAL

    def Run(self):
        while 1:
            self.sound.Play()
