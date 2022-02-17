import socket
import pickle
from game import Game
from _thread import *

server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection...")

connected = set()
players = [0, 0]
ready = [False, False]
updates = [False, False]
ships = [None, None]
game = None

def threaded_client(conn, p):
    global players, ready, updates, ships, game
    conn.send(str.encode(str(p)))
    pickled = False
    reply = ""
    pickledReply = None
    while True:
        try:
            if not pickled:
                data = conn.recv(2048).decode().split(":")
            else:
                data = pickle.loads(conn.recv(2048))
            if not data:
                print("No data received.")
                break
            else:
                reply = "None"
                pickledReply = None
                if pickled:
                    ships[p] = data
                    pickled = False
                elif data[0] == "get":
                    if data[1] == "players":
                        reply = f"{not 0 in players}:{ready[(p + 1) % 2]}:{game is not None}"
                    elif data[1] == "game":
                        reply = str(game)
                    elif data[1] == "turn":
                        reply = str(game.turn)
                    elif data[1] == "update":
                        reply = str(updates[p])
                        if updates[p]:
                            updates[p] = False
                    elif data[1] == "ships":
                        pickledReply = pickle.dumps(ships)
                elif data[0] == "play":
                    b, y, x = (p + 1) % 2, int(data[2]), int(data[1])
                    if game.boards[b][y][x] == 0:
                        hit = False
                        for ship in ships[b]:
                            if (x, y) in ship.get_positions():
                                hit = True
                                break
                        game.boards[b][y][x] = 1 if hit else 2
                        if not hit:
                            game.turn = (game.turn + 1) % 2
                    updates = [True, True]
                elif data[0] == "ready":
                    ready[p] = True
                elif data[0] == "unready":
                    ready[p] = False
                elif data[0] == "start":
                    if game is None:
                        game = Game()
                elif data[0] == "pickle":
                    pickled = True
                if pickledReply is None:
                    conn.send(str.encode(reply))
                else:
                    conn.send(pickledReply)
        except socket.error as e:
            print(e)
            break
    print("Lost Connection:", conn, "ID:", p)
    players[p] = 0
    conn.close()

while True:
    conn, addr = s.accept()
    
    p = -1
    for i in range(2):
        if players[i] == 0:
            p = i
            break
    players[p] = 1

    print("Connected to:", addr, "ID:", p)

    if p >= 0:
        start_new_thread(threaded_client, (conn, p))
    else:
        conn.send(str.encode(str(p)))