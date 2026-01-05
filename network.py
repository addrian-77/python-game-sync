import socket
import pickle

class Network:
    # create a new network
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # use localhost so far
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        # also call the connect function here
        self.connect()

    # connect to the network
    def connect(self):
        try:
            self.client.connect(self.addr)
        except:
            pass
    
    # send packets using pickle
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)