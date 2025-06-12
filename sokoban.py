import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
CELL_SIZE = 40
OFFSET = CELL_SIZE // 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

level = [
    "###########",
    "#  #     #",
    "#  ## ### #",
    "#    #   #",
    "## #######"
]

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Player(Entity):
    pass

class Box(Entity):
    pass

def load_level(level):
    walls = []
    targets = []
    boxes = []
    player = None
    
    for y in range(len(level)):
        for x in range(len(level[y])):
            cell = level[y][x]
            if cell == '#':
                walls.append((x, y))
            elif cell == '@':
                player = Player(x, y)
            elif cell == '$':
                boxes.append(Box(x, y))
            elif cell == '.':
                targets.append((x, y))
                
    return walls, targets, boxes, player

def draw_rect(color, x, y):
    pygame.draw.rect(screen, color, 
                     (x * CELL_SIZE + OFFSET//2,
                      y * CELL_SIZE + OFFSET//2,
                      CELL_SIZE - OFFSET,
                      CELL_SIZE - OFFSET))

walls, targets, boxes, player = load_level(level)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban")

def draw_game():
    screen.fill(BLACK)
    
    # Draw walls
    for (x, y) in walls:
        draw_rect(WHITE, x, y)
        
    # Draw targets
    for (x, y) in targets:
        if any(box.x == x and box.y == y for box in boxes):
            color = GREEN
        else:
            color = YELLOW
        pygame.draw.circle(screen, color, 
                          (x * CELL_SIZE + OFFSET, y * CELL_SIZE + OFFSET), 10)
        
    # Draw boxes
    for box in boxes:
        draw_rect(BLUE, box.x, box.y)
        
    # Draw player
    draw_rect(RED, player.x, player.y)

def move_entity(entity, dx, dy):
    if (entity.x + dx, entity.y + dy) not in walls and \
       -1 < entity.x + dx < len(level[0]) and \
       -1 < entity.y + dy < len(level):
        for box in boxes:
            if box.x == entity.x + dx and box.y == entity.y + dy:
                if (box.x + dx, box.y + dy) not in walls and \
                   -1 < box.x + dx < len(level[0]) and \
                   -1 < box.y + dy < len(level):
                    box.x += dx
                    box.y += dy
                    return True
        entity.x += dx
        entity.y += dy
    return False

def check_win():
    for (x, y) in targets:
        if not any(box.x == x and box.y == y for box in boxes):
            return False
    return True

running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        move_entity(player, -1, 0)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        move_entity(player, 1, 0)
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        move_entity(player, 0, -1)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        move_entity(player, 0, 1)
        
    draw_game()
    
    if check_win():
        font = pygame.font.Font(None, 36)
        text = font.render("WIN!", True, GREEN)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        
    pygame.display.flip()

pygame.quit()
sys.exit()
