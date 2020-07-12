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
