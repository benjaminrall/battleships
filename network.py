import socket

class Network():
    def __init__(self, server):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
    
    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.connected = True
            return self.client.recv(2048).decode()
        except socket.error as e:
            self.connected = False
            return -1

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            recv = self.client.recv(2048).decode()
            return recv
        except socket.error as e:
            print(str(e))