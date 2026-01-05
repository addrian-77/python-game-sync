# Multiplayer Pygame Shooter

A real-time multiplayer game foundation built using **Python**, **Pygame**, and **Sockets**. This project demonstrates how to implement a client-server architecture where multiple players can move simultaneously in a shared environment.

## 📂 Project Structure

This repository consists of three main files:

* **`server.py`**: The backend server script. It binds to `localhost` on port `5555` and listens for incoming connections. It uses threading to handle multiple clients simultaneously and acts as the central source of truth for the game state.
* **`game.py`**: The client-side application. It initializes the Pygame window (500x500) and handles user input and rendering. It continuously sends local coordinates to the server and receives the positions of other players.
* **`network.py`**: A helper class that manages the socket connection. It abstracts the complexity of sending and receiving data using Python's `pickle` library for serialization.

## ⚙️ Prerequisites

To run this project, you need Python installed along with the **Pygame** library.

```bash
pip install pygame
```

## 🚀 How to Run

To play the game, you must start the server first, and then run an instance of the client for each player.

### 1. Start the Server
Open your terminal and run the server script. This will start listening for connections.

```bash
python server.py
```
* The server runs on `localhost`, port `5555`.

### 2. Start the Clients
Open a new terminal window (one for each player) and run the game script.

```bash
python game.py
```

* **Player 1 (Host)**: Will appear as a **Red** square.
* **Player 2+**: Will appear as **Green** squares.

## 🎮 Controls

The game runs at 60 FPS. Use the keyboard arrows to move your character.

* **⬆️ Up Arrow**: Move Up
* **⬇️ Down Arrow**: Move Down
* **⬅️ Left Arrow**: Move Left
* **➡️ Right Arrow**: Move Right

## 🔧 Technical Details

* **Networking**: The project uses `socket.AF_INET` and `socket.SOCK_STREAM` for TCP connections.
* **Data Serialization**: The `pickle` module is used to serialize Python objects (dictionaries) so they can be sent over the network. The client sends a packet containing `{"x": x, "y": y}`, and the server responds with a dictionary containing all connected players.
* **Threading**: The server utilizes the `_thread` module to spawn a new thread for every client that connects, ensuring the main server loop is not blocked.