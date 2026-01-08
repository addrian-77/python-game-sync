import pygame
from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("shooter")

pygame.font.init()
font = pygame.font.SysFont("arialblack", 30)

def redrawWindow(win, players, bullets, my_id):
    win.fill((255,255,255))
    
    # draw bullets as circles
    for b in bullets:
        pygame.draw.circle(win, (0, 0, 0), (int(b["x"]), int(b["y"])), 5)

    for id, player in players.items():
        # extract color
        color = player["color"]    
        
        # draw player as a rectangle
        pygame.draw.rect(win, color, (player["x"], player["y"], 50, 50))

        # draw a healthbar
        # first draw a full red rectangle, then draw green over it
        pygame.draw.rect(win, (255, 0, 0), (player["x"], player["y"] - 10, 50, 5))
        hp_percent = max(0, player["hp"] / 100)
        pygame.draw.rect(win, (0, 255, 0), (player["x"], player["y"] - 10, 50 * hp_percent, 5))

        # create the score text
        score_text = font.render(f"Score: {player["score"]}", 1, (0, 0, 0))

        # if we're the player, place the text in the left corner
        # if not, place the score above the other player
        if id == my_id:
            win.blit(score_text, (10, 10))
        else:
            win.blit(score_text, (player["x"], player["y"] - 30))
        
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
    
            redrawWindow(win, game_state["players"], game_state["bullets"], player_id)
        
        except Exception as e:
            print("Error:", e)
            running = False


main()