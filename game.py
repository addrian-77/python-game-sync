import pygame
from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("shooter")

def redrawWindow(win, players):
    win.fill((255,255,255))
    
    for player in players.values():
        # extract color
        color = player["color"]    
        
        # draw player as a rectangle
        pygame.draw.rect(win, color, (player["x"], player["y"], 50, 50))
        
    pygame.display.update()

def main():
    running = True
    net = Network()
    player_id = net.pid
    print("pid")

    clock = pygame.time.Clock()
    
    # initial coordinates, size and velocity
    x, y = 250, 250
    width_p, height_p = 50, 50
    vel = 3
    
    
    while running:
        clock.tick(60)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        # get current frame inputs
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            x -= vel
        if keys[pygame.K_RIGHT]:
            x += vel
        if keys[pygame.K_UP]:
            y -= vel
        if keys[pygame.K_DOWN]:
            y += vel
            

        # limit player movement to window bounds
        x = max(0, min(x, 500 - width_p))
        y = max(0, min(y, 500 - height_p))

        packet_to_send = {
            "x" : x,
            "y" : y,
        }

        try:
            game_state = net.send(packet_to_send)

            redrawWindow(win, game_state["players"])
        
        except Exception as e:
            print("Error:", e)
            running = False


main()