# Handles all audio calls using pygame

import pygame.mixer

class Audio (object):
    def __init__(self):
        pygame.mixer.init()
        audio = {"jump": 0.5}
        self.audio = {}
        for key in audio.keys():
            print(key + ".wav")
            self.audio[key] = pygame.mixer.Sound(key + ".wav")
            self.audio[key].set_volume(audio[key])
    def playAudio(self, key):
        self.audio[key].play()