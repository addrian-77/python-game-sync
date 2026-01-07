import socket
from _thread import *
import pickle
import time

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

bullets = []

BULLET_SPEED = 10

def game_loop():
    while True:
        time.sleep(0.016) # 60fps

        # update bullets
        for b in bullets[:]:
            b["x"] += b["dir_x"] * BULLET_SPEED
            b["y"] += b["dir_y"] * BULLET_SPEED

            # remove bullet if it is out of bounds
            if b["x"] < 0 or b["x"] > 500 or b["y"] < 0 or b["y"] > 500:
                if b in bullets:
                    bullets.remove(b)
                continue

start_new_thread(game_loop, ())


def update_player(conn, current_player):
    # initialize the player
    if current_player == 0:
        color = [255, 0, 0]
    else:
        color = [0, 255, 0]
    players[current_player] = {
        "x": 250,
        "y": 250,
        "color": color,
        "facing_x": 1,
        "facing_y": 0
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
            players[current_player]["facing_x"] = data["facing"][0]
            players[current_player]["facing_y"] = data["facing"][1]

            # handle shooting
            if data["shoot"]:
                # establish the direction of the bullet
                dir_x = players[current_player]["facing_x"]
                dir_y = players[current_player]["facing_y"]
                
                # compute the position of the bullet
                # + 25 to place it at the center of the player
                bullet_x = players[current_player]["x"] + 25
                bullet_y = players[current_player]["y"] + 25

                bullets.append({
                    "x": bullet_x,
                    "y": bullet_y,
                    "dir_x": dir_x,
                    "dir_y": dir_y,
                    "owner_id": current_player 
                })

            # send back data
            game_state = {"players": players, "bullets": bullets}
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
