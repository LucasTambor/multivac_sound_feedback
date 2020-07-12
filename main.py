#!/usr/bin/python3
import time
import json
from logger import Logger
from mqttIPCHandler import MqttIPC
#sound
import pygame
import time

class Sound(object):
    CHANNEL_RIGHT = 0
    CHANNEL_LEFT = 1
    CHANNEL_CENTER = 2
    TONE_UP = 0
    TONE_DOWN = 1
    TONE_CENTER = 2

    MIN_INTERVAL = 0.4
    MAX_INTERVAL = 1
    def __init__(self):
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound('./sounds/beep_center.wav')
        self.channel = pygame.mixer.find_channel()

        # controle variable
        self.interval = self.MAX_INTERVAL
        self.status = False
        self.panLeft = 0.0
        self.panRight = 0.0

    def setPan(self, pan):
        if pan == self.CHANNEL_RIGHT:
            self.panLeft = 0.0
            self.panRight = 1.0
        elif pan == self.CHANNEL_LEFT:
            self.panLeft = 1.0
            self.panRight = 0.0
        elif pan == self.CHANNEL_CENTER:
            self.panLeft = 1.0
            self.panRight = 1.0
        else:
            self.panLeft = 0.0
            self.panRight = 0.0

    def setTone(self, tone):
        if tone == self.TONE_UP:
            self.sound = pygame.mixer.Sound('./sounds/beep_up.wav')
        elif tone == self.TONE_DOWN:
            self.sound = pygame.mixer.Sound('./sounds/beep_down.wav')
        elif tone == self.TONE_CENTER:
            self.sound = pygame.mixer.Sound('./sounds/beep_center.wav')
        else:
            pass

    def setStatus(self, status):
        self.status = status

    def setInterval(self, interval):
        self.interval = interval

    def Play(self):
        if self.status:
            self.channel.set_volume(self.panLeft, self.panRight)
            self.channel.play(self.sound)
            time.sleep(self.interval)


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

if __name__ == '__main__':
    mqtt = MqttIPC()
    sound = SoundHandle(mqtt)
    sound.Run()

