import pygame
from pygame.locals import *

pygame.init()

# Game constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 40
ROWS = 12
COLS = 16
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLUE
        self.size = CELL_SIZE // 2

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = RED
        self.on_target = False

def main():
    # Initialize game state
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    level = [
        "WWWWWWWWWWWWWWWW",
        "W............WW",
        "W.WWW.WWWW.W..W",
        "W.WWW.WWWW.W..W",
        "W.WWW.WWWW.W..W",
        "W..W......W..W",
        "W.WWW.WWWW.W..W",
        "W.WWW.WWWW.W..W",
        "W.WWW.WWWW.W..W",
        "W............WW",
        "WWWWWWWWWWWWWWWW"
    ]
    
    player = None
    boxes = []
    targets = []

    # Parse level layout
    for y in range(len(level)):
        for x in range(len(level[y])):
            cell = level[y][x]
            if cell == '@':
                player = Player(x, y)
            elif cell == '.':
                targets.append((x, y))
            elif cell == '#':
                boxes.append(Box(x, y))

    # Convert walls to coordinates
    walls = [(x, y) for y in range(len(level)) 
             for x in range(len(level[y])) if level[y][x] == 'W']

    def can_move(dx, dy):
        new_x = player.x + dx
        new_y = player.y + dy
        
        # Check wall collision
        if (new_x, new_y) in walls:
            return False
            
        # Check box collision
        for i, box in enumerate(boxes):
            if box.x == new_x and box.y == new_y:
                push_dir = dx, dy
                target_pos = (box.x + dx, box.y + dy)
                
                # Check if box can be pushed
                if target_pos not in walls and target_pos not in boxes:
                    return True
        
        return True

    def push_box(dx, dy):
        new_x = player.x + dx
        new_y = player.y + dy
        
        for i, box in enumerate(boxes):
            if box.x == new_x and box.y == new_y:
                # Update player position
                player.x += dx
                player.y += dy
                
                # Update box position
                box.x += dx
                box.y += dy
                
                return True

    def is_win():
        for box in boxes:
            if (box.x, box.y) not in targets or any(box == other_box for i, box in enumerate(boxes) for other_box in boxes[i+1:]):
                return False
        return True

    running = True
    while running:
        screen.fill(BLACK)

        # Draw walls
        for (x, y) in walls:
            pygame.draw.rect(screen, GRAY, 
                           (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

        # Draw targets
        for (x, y) in targets:
            pygame.draw.circle(screen, GREEN, 
                             (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2), 
                             CELL_SIZE//3)

        # Draw boxes
        for box in boxes:
            if not box.on_target:
                pygame.draw.rect(screen, RED, 
                               (box.x * CELL_SIZE, box.y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))
            else:
                pygame.draw.rect(screen, GREEN, 
                               (box.x * CELL_SIZE, box.y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

        # Draw player
        pygame.draw.circle(screen, BLUE,
                          (player.x * CELL_SIZE + CELL_SIZE//2, player.y * CELL_SIZE + CELL_SIZE//2),
                          CELL_SIZE//2)

        if is_win():
            font = pygame.font.Font(None, 48)
            text = font.render("WIN", True, GREEN)
            screen.blit(text, (SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT//2 - 20))
            pygame.display.flip()
            pygame.time.wait(2000)
            
            # Reset game
            player.x = 1
            player.y = 1
            boxes = [Box(x, y) for x in range(4,7) for y in range(3,6)]

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                
            elif event.type == KEYDOWN:
                dx, dy = 0, 0
                if (event.key == K_LEFT or event.key == K_a):
                    dx = -1
                elif (event.key == K_RIGHT or event.key == K_d):
                    dx = 1
                elif (event.key == K_UP or event.key == K_w):
                    dy = -1
                elif (event.key == K_DOWN or event.key == K_s):
                    dy = 1
                    
                if can_move(dx, dy):
                    player.x += dx
                    player.y += dy
                    
                    # Check if pushing a box
                    push_box(dx, dy)

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
