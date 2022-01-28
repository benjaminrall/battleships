import pygame
import os
from personallib.camera import Camera

from sprite_loader import Spritesheet

# Constants
WIN_WIDTH = 1000
WIN_HEIGHT = 650
FRAMERATE = 120
BOARD_SIZE = 400
SCALE = BOARD_SIZE // 10
ICON_IMG = pygame.image.load(os.path.join("imgs", "icon.png"))

# Pygame Setup
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Battleships")
pygame.display.set_icon(ICON_IMG)
clock = pygame.time.Clock()

# Objects
cam = Camera(win, 0, 0, 1)
playerSurface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
opponentSurface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
sprites = Spritesheet("imgs/sprites/", SCALE)

class Ship:
    def __init__(self, t, pos=(-1, -1), inTray=True):
        self.state = -1
        self.root = pos
        self.type = t
        self.orientation = 0
        self.inTray = inTray

class Tray:
    def __init__(self, x, y, w, h):
        self.surface = pygame.Surface((w, h))
        self.pos = (x, y)
        self.ships = [Ship(i) for i in range(5)]

    def __getitem__(self, i):
        return self.ships[i]

    def within_tray(self, pos):
        return False

    def get_tray_index(self, pos):
        return False

    def draw(self, cam):
        self.surface.fill((100, 100, 100))
        for i, ship in enumerate(self):
            pygame.draw.rect(self.surface, (255, 255, 255), (30 + (75 * i), 30, 40, 40))
        cam.blit(self.surface, self.pos)


tray = Tray(-440, 165, BOARD_SIZE, BOARD_SIZE // 4)

# Variables
running = True
heldShip = None

# Methods
def draw_player_board(cam, surface, ships, heldShip):
    surface.fill((100, 100, 100))
    for ship in ships:
        if ship != heldShip:
            surface.blit(sprites[(ship.type * 2) + ship.orientation], (ship.root[0] * SCALE, ship.root[1] * SCALE))
    cam.blit(surface, (-440, -265))

# Main Loop
if __name__ == '__main__':
    while running:

        clock.tick(FRAMERATE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    print(mousePos, cam.get_screen_coord(tray.pos))
                    
        win.fill((50, 50, 50))
        opponentSurface.fill((100, 100, 100))



        tray.draw(cam)
        draw_player_board(cam, playerSurface, [Ship(0, (1, 1), False)], None)
        
        cam.blit(opponentSurface, (40, -265))
        
        pygame.display.update()