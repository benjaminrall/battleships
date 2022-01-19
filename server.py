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
storedFen = "none"
storedHeldPiece = "none"

def threaded_client(conn, p):
    global storedFen
    global storedHeldPiece
    conn.send(str.encode(str(p)))
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                print("e3")
                break
            else:                    
                
                reply = ""
                conn.send(str.encode(reply))
        except socket.error as e:
            print(e)
            break
    print("Lost connection", conn)
    players[p] = 0
    if not 1 in players:
        storedFen = "none"
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:",addr)
    
    p = -1
    for i in range(2):
        if players[i] == 0:
            p = i
    players[p] = 1

    if p >= 0:
        start_new_thread(threaded_client, (conn, p))
    else:
        conn.send(str.encode(str(p)))