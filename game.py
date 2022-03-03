import random

class Game:
    def __init__(self, game=""):
        if game == "None":
            raise Exception("Cannot create 'None' game.")
        new = game == ""
        game = game.split("~")
        self.turn = random.randint(0, 1) if new else int(game[0])
        self.boards = [
            [[0 for _ in range(10)] for _ in range(10)] if new else [[int(e) for e in row.split("|")] for row in game[1].split(":")],
            [[0 for _ in range(10)] for _ in range(10)] if new else [[int(e) for e in row.split("|")] for row in game[2].split(":")]
        ]
        self.lastTurn = None if new or (not new and game[3] == "None") else [int(e) for e in game[3].split(":")]
        self.winner = -1 if new else int(game[4])

    def __str__(self):
        board1 = ':'.join(['|'.join([str(e) for e in row]) for row in self.boards[0]])
        board2 = ':'.join(['|'.join([str(e) for e in row]) for row in self.boards[1]])
        lastTurn = "None" if self.lastTurn is None else f"{self.lastTurn[0]}:{self.lastTurn[1]}"
        return f"{self.turn}~{board1}~{board2}~{lastTurn}~{self.winner}"