import pygame
import sys

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
    global targets
    # Example level setup (adjust as needed)
    boxes = []
    targets = [(1, 1), (2, 3)]  # Define target positions

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
            if event.key == pygame.K_LEFT and new_x > 0:
                new_x -= 1
            elif event.key == pygame.K_RIGHT and new_x < (SCREEN_WIDTH // CELL_SIZE) - 1:
                new_x += 1
            elif event.key == pygame.K_UP and new_y > 0:
                new_y -= 1
            elif event.key == pygame.K_DOWN and new_y < (SCREEN_HEIGHT // CELL_SIZE) - 1:
                new_y += 1

            # Check if movement affects any boxes
            moved = False
            for box in boxes:
                if (box.x, box.y) == (new_x, new_y):
                    # Try to push the box
                    next_x, next_y = new_x + (player.x - box.x), new_y + (player.y - box.y)
                    if 0 <= next_x < (SCREEN_WIDTH // CELL_SIZE) and 0 <= next_y < (SCREEN_HEIGHT // CELL_SIZE):
                        if not any((b.x == next_x and b.y == next_y) for b in boxes if b != box):
                            box.x, box.y = next_x, next_y
                            moved = True

            # Only move player if movement didn't result in pushing a box (or space is empty)
            if not moved:
                player.x, player.y = new_x, new_y

    screen.fill(WHITE)

    draw_grid(screen)

    for box in boxes:
        box.draw(screen)

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
