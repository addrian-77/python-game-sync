import socket
from _thread import *
import pickle

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection")


def update_player(conn):
    # initialize the player
    player = {
        "x": 250,
        "y": 250,
    }

    # keep updating the player
    while True:
        try:
            # receive data from the client
            data = pickle.loads(conn.recv(4096))

            if not data:
                break
            
            # update player
            player["x"] = data["x"]
            player["y"] = data["y"]

            # send back data
            conn.sendall(pickle.dumps(player))
        except Exception as e:
            print(e)
            break
    
    print("Lost connection")
    conn.close()

# accept new connections indefinetly
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    # start a thread for each connection
    start_new_thread(update_player, (conn,))
