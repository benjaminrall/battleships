from ship import Ship

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(10)]
        self.ships = [Ship(5, 0), Ship(4, 1), Ship(3, 2), Ship(3, 3), Ship(2, 4)]