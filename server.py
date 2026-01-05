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

players = {}

def update_player(conn, current_player):
    # initialize the player
    if current_player == 0:
        color = [255, 0, 0]
    else:
        color = [0, 255, 0]
    players[current_player] = {
        "x": 250,
        "y": 250,
        "color": color
    }

    # send the player id on init
    conn.send(pickle.dumps(current_player))

    # keep updating the player
    while True:
        try:
            # receive data from the client
            data = pickle.loads(conn.recv(4096))

            if not data:
                break
            
            # update player
            players[current_player]["x"] = data["x"]
            players[current_player]["y"] = data["y"]

            # send back data
            game_state = {"players": players,}
            conn.sendall(pickle.dumps(game_state))
        except Exception as e:
            print(e)
            break
    
    print("Lost connection")
    
    # remove the player
    if current_player in players:
        del(players[current_player])
    # close the connection
    conn.close()

player_count = 0
# accept new connections indefinetly
while True:
    conn, addr = s.accept()
    print("Player ", player_count, " connected to: ", addr)
    # start a thread for each connection
    start_new_thread(update_player, (conn, player_count))
    player_count += 1
