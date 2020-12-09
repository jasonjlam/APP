# Handles all audio calls using pygame

import pygame.mixer
import atexit

class Audio (object):
    def __init__(self):
        pygame.mixer.init()
        audio = {"jump": 0.5, 'shoot': 0.1, 'wallHit': 0.2, 'enemyHit': 0.2,
        "gastly": 0.15, "haunter": 0.15}
        self.audio = {}
        for key in audio.keys():
            self.audio[key] = pygame.mixer.Sound(f"assets/sounds/{key}.wav")
            self.audio[key].set_volume(audio[key])

    def playAudio(self, key):
        self.audio[key].play()
    def playMusic(self, key, volume):
        pygame.mixer.music.load(f"assets/music/{key}")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)
