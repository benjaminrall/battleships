import pygame
import os

class Spritesheet:
    def __init__(self, path):
        self.sprites = []
        for file in os.listdir(path):
            self.sprites.append(pygame.image.load(path + file))
        
    def __getitem__(self, i):
        return self.sprites[i]