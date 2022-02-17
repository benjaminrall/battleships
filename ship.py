class Ship:

    sizes = [
        [(0, 3),(3, 0)],  # battleship
        [(0, 4),(4, 0)],  # carrier
        [(0, 2),(2, 0)],  # cruiser
        [(0, 1),(1, 0)],  # destroyer
        [(0, 2),(2, 0)]   # submarine
    ]

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

    def get_positions(self, root = None):
        if root is None:
            root = self.root
        size = Ship.sizes[self.type][self.orientation]
        length = max(size) + 1
        index = 0 if size[0] > size[1] else 1
        positions = []
        for i in range(length):
            tempPos = [root[0], root[1]]
            tempPos[index] += i
            positions.append(tuple(tempPos))
        return positions

    def overlaps(self, ships, root = None):
        positions = self.get_positions(root)
        overlap = False
        for ship in ships:
            if self is not ship:
                shipPositions = ship.get_positions()
                for position in positions:
                    if position in shipPositions:
                        overlap = True
                        break
        return overlap