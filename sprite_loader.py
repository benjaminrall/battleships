import pygame
import os

class Spritesheet:
    def __init__(self, path, desiredSize):
        self.sprites = []
        for file in os.listdir(path):
            image = pygame.image.load(path + file)
            size = image.get_size()
            multiplier = desiredSize / min(size)
            newSize = (int(size[0] * multiplier), int(size[1] * multiplier))
            self.sprites.append(pygame.transform.scale(image, newSize))
        
    def __getitem__(self, i):
        return self.sprites[i]

#s = Spritesheet("imgs/sprites/", 40)