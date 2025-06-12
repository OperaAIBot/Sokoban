import pygame
import sys

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
CELL_SIZE = 20
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Player(Entity):
    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x * CELL_SIZE + CELL_SIZE//2, self.y * CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)

class Box(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.target = False

    def draw(self):
        color = RED if not self.target else GREEN
        pygame.draw.rect(screen, color, (self.x * CELL_SIZE + CELL_SIZE//4, self.y * CELL_SIZE + CELL_SIZE//4, CELL_SIZE//2, CELL_SIZE//2))

class Wall(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.blocked = True

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def create_level():
    global player, boxes, targets
    # Create walls
    walls = [[True if x == 0 or x == (SCREEN_WIDTH//CELL_SIZE)-1 else False for y in range(SCREEN_HEIGHT//CELL_SIZE)] for x in range(SCREEN_WIDTH//CELL_SIZE)]
    for x in range(SCREEN_WIDTH//CELL_SIZE):
        for y in range(SCREEN_HEIGHT//CELL_SIZE):
            if walls[x][y]:
                Wall(x, y)
    
    # Create player
    player = Player(3, 2)
    
    # Create boxes and targets
    boxes = [Box(2,2), Box(3,3)]
    targets = [(1,1), (4,4)]
    for box in boxes:
        if (box.x, box.y) in targets:
            box.target = True

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

def check_win():
    return all((box.x, box.y) in targets for box in boxes)

def move_player(dx, dy):
    new_x = player.x + dx
    new_y = player.y + dy
    
    # Check if moving into a wall or box
    blocked = False
    for entity in [player] + walls:
        if isinstance(entity, Wall) and (new_x == entity.x and new_y == entity.y):
            blocked = True
            break
    
    if not blocked:
        for i, box in enumerate(boxes):
            if box.x == player.x + dx and box.y == player.y + dy:
                # Try to push box
                next_cell_x = box.x + dx
                next_cell_y = box.y + dy
                can_push = True
                
                # Check if pushing into wall or another box
                for e in walls + boxes:
                    if isinstance(e, Wall) and (next_cell_x == e.x and next_cell_y == e.y):
                        can_push = False
                        break
                    if isinstance(e, Box) and (e != box) and (next_cell_x == e.x and next_cell_y == e.y):
                        can_push = False
                        break
                
                if can_push:
                    boxes[i].x += dx
                    boxes[i].y += dy
                    blocked = True  # Prevent player from moving through pushed box
        
        if not blocked:
            player.x = new_x
            player.y = new_y

# Game setup
walls = []
boxes = []
targets = []
create_level()

while True:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            dx, dy = 0, 0
            if (event.key == pygame.K_LEFT or event.key == ord('a')):
                dx = -1
            elif (event.key == pygame.K_RIGHT or event.key == ord('d')):
                dx = 1
            elif (event.key == pygame.K_UP or event.key == ord('w')):
                dy = -1
            elif (event.key == pygame.K_DOWN or event.key == ord('s')):
                dy = 1
            
            move_player(dx, dy)
    
    # Draw all elements
    draw_grid()
    player.draw()
    
    for box in boxes:
        box.draw()
    
    for wall in walls:
        wall.draw()
    
    if check_win():
        font = pygame.font.Font(None, 36)
        text = font.render("You Win!", True, GREEN)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    
    pygame.display.flip()
    clock.tick(FPS)
