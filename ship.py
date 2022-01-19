import random
import copy

class Ship:
    def __init__(self, n, board):
        self.length = n
        self.board = board
        self.orientation = 0
        self.root = []
        valid = False
        while not valid:
            self.randomise_position()
            coords = self.calculate_coords()
            valid = not False in [board.grid[coord[0]][coord[1]] == 0 for coord in coords]
        self.bounds = self.calculate_bounds()
        self.coords = coords

    def randomise_position(self):
        self.orientation = random.randint(0, 1)
        self.root = [random.randint(0, 9 - self.length), random.randint(0, 9 - self.length)]

    def calculate_bounds(self):
        end = copy.copy(self.root)
        end[self.orientation] += (self.length - 1)
        return [(self.root[0], end[0]), (self.root[1], end[1])]

    def calculate_coords(self):
        coords = [(self.root[0] + i if self.orientation == 0 else self.root[0], self.root[1] + i if self.orientation == 1 else self.root[1]) for i in range(self.length)]
        return coords

ship = Ship(5)
print(ship.coords)