import pygame
from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("shooter")

def redrawWindow(win, players, bullets):
    win.fill((255,255,255))
    
    # draw bullets as circles
    for b in bullets:
        pygame.draw.circle(win, (0, 0, 0), (int(b["x"]), int(b["y"])), 5)

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
    facing_x, facing_y  = 1, 0
    vel = 3
    
    shoot_timer = 0

    while running:
        clock.tick(60)
        
        shoot_cmd = False
        if shoot_timer > 0:
            shoot_timer -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        # get current frame inputs
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            x -= vel
            facing_x = -1
            facing_y = 0
        if keys[pygame.K_RIGHT]:
            x += vel
            facing_x = 1
            facing_y = 0
        if keys[pygame.K_UP]:
            y -= vel
            facing_x = 0
            facing_y = -1
        if keys[pygame.K_DOWN]:
            y += vel
            facing_x = 0
            facing_y = 1

        if keys[pygame.K_SPACE] and shoot_timer == 0:
            shoot_cmd = True
            shoot_timer = 20

            

        # limit player movement to window bounds
        x = max(0, min(x, 500 - width_p))
        y = max(0, min(y, 500 - height_p))

        packet_to_send = {
            "x": x,
            "y": y,
            "shoot": shoot_cmd,
            "facing": (facing_x, facing_y)
        }

        try:
            # send the packet and receive the game state containing data about players and bullets
            game_state = net.send(packet_to_send)

            redrawWindow(win, game_state["players"], game_state["bullets"])
        
        except Exception as e:
            print("Error:", e)
            running = False


main()