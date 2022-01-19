import pygame
import os
from personallib.camera import Camera

# Constants
WIN_WIDTH = 1000
WIN_HEIGHT = 600
FRAMERATE = 120
ICON_IMG = pygame.image.load(os.path.join("imgs", "icon.png"))

# Pygame Setup
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Battleships")
pygame.display.set_icon(ICON_IMG)
clock = pygame.time.Clock()

# Objects
cam = Camera(win, 0, 0, 1)
playerSurface = pygame.Surface((400, 400))
opponentSurface = pygame.Surface((400, 400))

# Variables
running = True

# Methods
def 

# Main Loop
if __name__ == '__main__':
    while running:

        clock.tick(FRAMERATE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
                    
        win.fill((50, 50, 50))
        playerSurface.fill((100, 100, 100))
        opponentSurface.fill((100, 100, 100))
        cam.blit(playerSurface, (-440, -200))
        cam.blit(opponentSurface, (40, -200))
        pygame.display.update()