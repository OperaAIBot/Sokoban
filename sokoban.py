import pygame
import sys

from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
CELL_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Global targets list
targets = []
walls = []

def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target = False

    def draw(self, screen):
        # Determine the color based on current position
        if (self.x, self.y) in targets:
            color = GREEN
        else:
            color = RED
        pygame.draw.rect(screen, color, 
                         [self.x * CELL_SIZE, self.y * CELL_SIZE, 
                          CELL_SIZE - 1, CELL_SIZE - 1])

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, 
                         [self.x * CELL_SIZE, self.y * CELL_SIZE, 
                          CELL_SIZE - 1, CELL_SIZE - 1])

def create_level():
    global targets, walls
    # Example level setup (adjust as needed)
    boxes = []
    targets = [(1, 1), (2, 3)]  # Define target positions
    walls = [(0, 1), (1, 0), (3, 3)]  # Define wall positions

    # Add some boxes (example positions)
    boxes.append(Box(0, 1))
    boxes.append(Box(1, 2))

    player = Player(0, 0)

    return boxes, player

def check_win():
    for box in boxes:
        if (box.x, box.y) not in targets:
            return False
    return True

# Set up the level
boxes, player = create_level()

# Main game loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Box Puzzle Game")

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Handle player movement (example)
            new_x, new_y = player.x, player.y
            dx, dy = 0, 0

            if event.key == K_LEFT:
                dx -= 1
            elif event.key == K_RIGHT:
                dx += 1
            elif event.key == K_UP:
                dy -= 1
            elif event.key == K_DOWN:
                dy += 1

            new_x = player.x + dx
            new_y = player.y + dy

            # Check if movement is within bounds and not into a wall
            if (new_x, new_y) in walls or new_x < 0 or new_x >= (SCREEN_WIDTH // CELL_SIZE) or new_y < 0 or new_y >= (SCREEN_HEIGHT // CELL_SIZE):
                continue

            # Check if movement affects any boxes
            moved = False
            for box in boxes:
                if (box.x, box.y) == (new_x, new_y):
                    # Try to push the box
                    next_x = new_x + dx
                    next_y = new_y + dy
                    if 0 <= next_x < (SCREEN_WIDTH // CELL_SIZE) and 0 <= next_y < (SCREEN_HEIGHT // CELL_SIZE):
                        if not any((b.x == next_x and b.y == next_y) for b in boxes if b != box) and (next_x, next_y) not in walls:
                            box.x, box.y = next_x, next_y
                            moved = True

            # Only move player if movement didn't result in pushing a box (or space is empty)
            if not moved:
                player.x, player.y = new_x, new_y

    screen.fill(WHITE)

    draw_grid(screen)

    for box in boxes:
        box.draw(screen)

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, BLACK, [wall[0] * CELL_SIZE, wall[1] * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1])

    player.draw(screen)

    # Update each box's target attribute based on current position
    for box in boxes:
        box.target = (box.x, box.y) in targets

    # Check if all boxes are on targets
    if check_win():
        print("You Win!")
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
