#!/usr/bin/python3
from mqttIPCHandler import MqttIPC
from soundHandler import SoundHandle


if __name__ == '__main__':
    mqtt = MqttIPC()
    sound = SoundHandle(mqtt)
    sound.Run()

