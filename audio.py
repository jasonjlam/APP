# Handles all audio calls using pygame

import pygame.mixer

class Audio (object):
    def __init__(self):
        pygame.mixer.init()
        self.jump = pygame.mixer.Sound("jump.wav")

    def jumpAudio(self):
        self.jump.play()