import socket
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

def threaded_client(conn, p):
    conn.send(str.encode(str(p)))
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode().split(":")
            if not data:
                print("No data received.")
                break
            else:
                reply = "Invalid Request"
                if data[0] == "get":
                    if data[1] == "players":
                        reply = f"{not 0 in players}:{ready[(p + 1) % 2]}: "
                elif data[0] == "ready":
                    ready[p] = True
                elif data[0] == "unready":
                    ready[p] = False
                conn.send(str.encode(reply))
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

    print(players)

    print("Connected to:", addr, "ID:", p)

    if p >= 0:
        start_new_thread(threaded_client, (conn, p))
    else:
        conn.send(str.encode(str(p)))