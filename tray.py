import pygame
from ship import Ship

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
        relX = pos[0] - self.pos[0]
        i = int((relX - 13) // 75)
        return max(min(i, 4), 0)

    def draw(self, cam, heldShip, sprites):
        if len(self.ships) <= 0:
            return
        self.surface.fill((100, 100, 100))
        for i, ship in enumerate(self):
            if (ship != heldShip):
                self.surface.blit(sprites[(ship.type * 2) + ship.orientation], (30 + (75 * i), 30))
        cam.blit(self.surface, self.pos)