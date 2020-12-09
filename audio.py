# Handles all audio calls using pygame

import pygame.mixer

class Audio (object):
    def __init__(self):
        pygame.mixer.init()
        audio = {"jump": 0.5, "death" : 0.25, 'shoot': 0.1, 'wallHit': 0.07, 'enemyHit': 0.1}
        self.audio = {}
        for key in audio.keys():
            self.audio[key] = pygame.mixer.Sound(f"assets/sounds/{key}.wav")
            self.audio[key].set_volume(audio[key])
    def playAudio(self, key):
        self.audio[key].play()