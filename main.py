import pygame
import os
from personallib.camera import Camera

from sprite_loader import Spritesheet

# Constants
WIN_WIDTH = 1000
WIN_HEIGHT = 650
FRAMERATE = 120
GRID_SIZE = 400
SCALE = GRID_SIZE // 10
ICON_IMG = pygame.image.load(os.path.join("imgs", "icon.png"))

# Pygame Setup
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Battleships")
pygame.display.set_icon(ICON_IMG)
clock = pygame.time.Clock()

# Objects
cam = Camera(win, 0, 0, 1)
playerSurface = pygame.Surface((GRID_SIZE, GRID_SIZE))
opponentSurface = pygame.Surface((GRID_SIZE, GRID_SIZE))
sprites = Spritesheet("imgs/sprites/", SCALE)

class Ship:

    sizes = {
        0:[(0, 3),(3, 0)],  # battleship
        1:[(0, 4),(4, 0)],  # carrier
        2:[(0, 2),(2, 0)],  # cruiser
        3:[(0, 1),(1, 0)],  # destroyer
        4:[(0, 2),(2, 0)]   # submarine
    }

    def __init__(self, t, pos=(-1, -1), inTray=True):
        self.state = -1
        self.root = pos
        self.type = t
        self.orientation = 0
        self.inTray = inTray

    def get_bounds(self, root = None):
        if root is None:
            root = self.root
        size = Ship.sizes[self.type][self.orientation]
        end = (root[0] + size[0], root[1] + size[1])
        return (root, end)

    def get_positions(self):
        return None

    def overlaps(self, ships):
        bounds = self.get_bounds()
        print(bounds)
        print(max(bounds[1]))
        for i in range(max(Ship.sizes[self.type][self.orientation]) + 1):
            print(i)
        return False

class Tray:
    def __init__(self, x, y, w, h):
        self.pos = (x, y)
        self.dimensions = (w, h)
        self.surface = pygame.Surface(self.dimensions)
        self.ships = [Ship(i) for i in range(5)]

    def __getitem__(self, i):
        return self.ships[i]

    def contains_pos(self, pos):
        relX = pos[0] - self.pos[0] 
        relY = pos[1] - self.pos[1]
        if 0 <= relX < self.dimensions[0] and 0 <= relY < self.dimensions[1]:
            return True
        return False

    def get_tray_index(self, pos):
        # 30-70, 105-145, 180-220, 255-295, 330-370
        # 0: x < 88
        # 1: 88 <= x < 163
        # 2: 163 <= x < 238
        # 3: 238 <= x < 313
        # 4: 313 <= x
        relX = pos[0] - self.pos[0]
        i = int((relX - 13) // 75)
        return max(min(i, 4), 0)

    def draw(self, cam, heldShip):
        if len(self.ships) <= 0:
            return
        self.surface.fill((100, 100, 100))
        for i, ship in enumerate(self):
            if (ship != heldShip):
                self.surface.blit(sprites[(ship.type * 2) + ship.orientation], (30 + (75 * i), 30))
        cam.blit(self.surface, self.pos)


tray = Tray(40, -265, GRID_SIZE, GRID_SIZE // 4 + SCALE * 4)

# Variables
running = True
heldShip = None
heldShipOrientation = 0
playerShips = []

# Methods
def draw_player_board(cam, surface, ships, heldShip):
    surface.fill((0, 0, 60))
    for y in range(10):
        for x in range(10):
            pygame.draw.rect(surface, (0, 0, 200), (x * SCALE + 1, y * SCALE + 1, SCALE - 2, SCALE - 2))
    for ship in ships:
        if ship != heldShip:
            surface.blit(sprites[(ship.type * 2) + ship.orientation], (ship.root[0] * SCALE, ship.root[1] * SCALE))
    cam.blit(surface, (-440, -265))
    if heldShip is not None:
        mousePos = cam.get_world_coord(pygame.mouse.get_pos())
        sprite = sprites[(heldShip.type * 2) + heldShip.orientation]
        cam.blit(sprite, (mousePos[0] - SCALE // 2, mousePos[1] - SCALE // 2))

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
                    mousePos = cam.get_world_coord(pygame.mouse.get_pos())
                    gridPos = (-440, -265)
                    relX = mousePos[0] - gridPos[0]
                    relY = mousePos[1] - gridPos[1]
                    if tray.contains_pos(mousePos):
                        heldShip = tray[tray.get_tray_index(mousePos)]
                    elif 0 <= relX < GRID_SIZE and 0 <= relY < GRID_SIZE:
                        newPos = (relX // SCALE, relY // SCALE)
                        for ship in playerShips:
                            bounds = ship.get_bounds()
                            if bounds[0][0] <= newPos[0] <= bounds[1][0] and bounds[0][1] <= newPos[1] <= bounds[1][1]:
                                heldShip = ship
                                break
                    if heldShip is not None:
                        heldShipOrientation = heldShip.orientation
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and heldShip is not None:
                    validDrop = False
                    mousePos = cam.get_world_coord(pygame.mouse.get_pos())
                    gridPos = (-440, -265)
                    relX = mousePos[0] - gridPos[0]
                    relY = mousePos[1] - gridPos[1]
                    if 0 <= relX < GRID_SIZE and 0 <= relY < GRID_SIZE:
                        newPos = (relX // SCALE, relY // SCALE)
                        newBounds = heldShip.get_bounds(newPos)
                        if 0 <= newBounds[1][0] < 10 and 0 <= newBounds[1][1] < 10 and not heldShip.overlaps(playerShips):
                            heldShip.root = newPos
                            validDrop = True
                            if heldShip.inTray:
                                playerShips.append(heldShip)
                                tray.ships.remove(heldShip)
                                heldShip.inTray = False
                    if not validDrop:
                        heldShip.orientation = heldShipOrientation
                    heldShip = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and heldShip is not None:
                    heldShip.orientation = (heldShip.orientation + 1) % 2
                        
                    
        win.fill((50, 50, 50))
        opponentSurface.fill((100, 100, 100))

        tray.draw(cam, heldShip)

        #cam.blit(opponentSurface, (40, -265))
    
        draw_player_board(cam, playerSurface, playerShips, heldShip)
        
        pygame.display.update()