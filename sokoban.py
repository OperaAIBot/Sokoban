import pygame
from pygame.locals import *
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Tile size
TILE_SIZE = 32

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Player and box properties
PLAYER_SPEED = 5
BOX_SPEED = 4

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = None
        self.speed = PLAYER_SPEED
        
    def move(self, dx=0, dy=0):
        self.x += dx * self.speed
        self.y += dy * self.speed
        
    def draw(self):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), TILE_SIZE // 2)

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moving = False
        self.speed = BOX_SPEED
        
    def move(self, dx=0, dy=0):
        if self.moving:
            self.x += dx * self.speed
            self.y += dy * self.speed
            
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x - TILE_SIZE//2, self.y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE))

class SokobanGame:
    def __init__(self):
        self.levels = [
            [
                "#########",
                "# @  B #",
                "#. .   #",
                "#########"
            ],
            [
                "##########",
                "# @ B   #",
                "#  . B .#",
                "#.      #",
                "##########"
            ],
            [
                "#############",
                "# @   B     #",
                "#  B .  B   #",
                "#.    .    .#",
                "#############"
            ]
        ]
        
        self.current_level = 0
        self.player = None
        self.boxes = []
        self.targets = []
        self.walls = []
        
    def load_level(self):
        level = self.levels[self.current_level]
        self.player = None
        self.boxes.clear()
        self.targets.clear()
        self.walls.clear()
        
        for y in range(len(level)):
            for x in range(len(level[y])):
                pos_x = x * TILE_SIZE + (TILE_SIZE // 2)
                pos_y = y * TILE_SIZE + (TILE_SIZE // 2)
                
                if level[y][x] == '#':
                    self.walls.append((pos_x, pos_y))
                elif level[y][x] == '@':
                    self.player = Player(pos_x, pos_y)
                elif level[y][x] == 'B':
                    self.boxes.append(Box(pos_x, pos_y))
                elif level[y][x] == '.':
                    self.targets.append((pos_x, pos_y))
        
    def check_win(self):
        for box in self.boxes:
            if (box.x, box.y) not in [(t[0], t[1]) for t in self.targets]:
                return False
        return True
        
    def draw_grid(self):
        for y in range(HEIGHT // TILE_SIZE + 1):
            pygame.draw.line(screen, GRAY, (0, y * TILE_SIZE), (WIDTH, y * TILE_SIZE))
        for x in range(WIDTH // TILE_SIZE + 1):
            pygame.draw.line(screen, GRAY, (x * TILE_SIZE, 0), (x * TILE_SIZE, HEIGHT))

# Initialize game
game = SokobanGame()
clock = pygame.time.Clock()

def main():
    while True:
        screen.fill(BLACK)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        # Get input
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[K_UP] or keys[K_w]:
            dy = -1
        elif keys[K_DOWN] or keys[K_s]:
            dy = 1
        if keys[K_LEFT] or keys[K_a]:
            dx = -1
        elif keys[K_RIGHT] or keys[K_d]:
            dx = 1
            
        # Move player and boxes
        game.player.move(dx * game.player.speed, dy * game.player.speed)
        
        for box in game.boxes:
            if not box.moving:
                box_x_dist = abs(box.x - game.player.x)
                box_y_dist = abs(box.y - game.player.y)
                
                if (box_x_dist < TILE_SIZE and box_y_dist < TILE_SIZE):
                    if dx != 0 or dy != 0:
                        box.direction = (dx, dy)
                        box.moving = True
                        
            if box.moving:
                box.move(*box.direction)
        
        # Draw everything
        game.draw_grid()
        
        for wall in game.walls:
            pygame.draw.rect(screen, GRAY, (wall[0] - TILE_SIZE//2, wall[1] - TILE_SIZE//2, TILE_SIZE, TILE_SIZE))
            
        for target in game.targets:
            pygame.draw.circle(screen, RED, (target[0], target[1]), TILE_SIZE // 3)
            
        for box in game.boxes:
            box.draw()
        
        game.player.draw()
        
        # Check win condition
        if game.check_win():
            print("Level complete!")
            game.current_level += 1
            
            if game.current_level >= len(game.levels):
                print("Congratulations! You won the game!")
                pygame.quit()
                sys.exit()
                
            game.load_level()
            
        # Update screen
        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    main()
