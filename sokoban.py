import pygame
from pygame.locals import *
import sys

pygame.init()

# Game constants
CELL_SIZE = 40
WALL_WIDTH = 20
PLAYER_RADIUS = 15
BOX_SIZE = 30
TARGET_RADIUS = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen setup
SCREEN_WIDTH = 8 * CELL_SIZE
SCREEN_HEIGHT = 6 * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban")

# Clock for frame rate
clock = pygame.time.Clock()

# Player properties
player_pos = {
    "x": 2 * CELL_SIZE,
    "y": 2 * CELL_SIZE
}
player_speed = 3

# Level setup
walls = []
boxes = []
targets = []

# Define level layout (1: wall, 2: box, 3: target)
level_layout = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 3, 2, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 3, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# Initialize game elements
for y in range(6):
    for x in range(8):
        if level_layout[y][x] == 1:
            wall_rect = pygame.Rect(
                x * CELL_SIZE - WALL_WIDTH // 2,
                y * CELL_SIZE - WALL_WIDTH // 2,
                WALL_WIDTH, WALL_WIDTH
            )
            walls.append(wall_rect)
        elif level_layout[y][x] == 2:
            box_rect = pygame.Rect(
                x * CELL_SIZE - BOX_SIZE // 2 + CELL_SIZE % 2,
                y * CELL_SIZE - BOX_SIZE // 2 + CELL_SIZE % 2,
                BOX_SIZE, BOX_SIZE
            )
            boxes.append(box_rect)
        elif level_layout[y][x] == 3:
            target_center = (
                x * CELL_SIZE,
                y * CELL_SIZE
            )
            targets.append(target_center)

# Movement variables
move_x = 0
move_y = 0

def check_box_collision(player, box):
    player_rect = pygame.Rect(
        player["x"] - PLAYER_RADIUS*2,
        player["y"] - PLAYER_RADIUS*2,
        PLAYER_RADIUS*4, PLAYER_RADIUS*4
    )
    return player_rect.colliderect(box)

def move_player(dx, dy):
    global player_pos
    new_x = player_pos['x'] + dx * player_speed
    new_y = player_pos['y'] + dy * player_speed

    # Check for collisions with walls
    test_player_rect = pygame.Rect(
        new_x - PLAYER_RADIUS*2,
        new_y - PLAYER_RADIUS*2,
        PLAYER_RADIUS*4, PLAYER_RADIUS*4
    )
    
    collision_wall = False
    for wall in walls:
        if test_player_rect.colliderect(wall):
            collision_wall = True
    
    # Check for collisions with boxes
    collision_box = None
    for i, box in enumerate(boxes):
        if check_box_collision({'x': new_x, 'y': new_y}, box):
            collision_box = i

    if collision_wall or (collision_box is not None and not can_push_box(collision_box, dx, dy)):
        return
    
    player_pos['x'] = new_x
    player_pos['y'] = new_y

    # Move boxes if pushed
    for i, box in enumerate(boxes):
        if check_box_collision(player_pos, box) and collision_box == i:
            new_box_x = box.x + dx * player_speed
            new_box_y = box.y + dy * player_speed
            test_box_rect = pygame.Rect(
                new_box_x - BOX_SIZE // 2,
                new_box_y - BOX_SIZE // 2,
                BOX_SIZE, BOX_SIZE
            )
            
            # Check if new box position is valid
            valid_move = True
            for wall in walls:
                if test_box_rect.colliderect(wall):
                    valid_move = False
            
            for other_box in boxes[:i] + boxes[i+1:]:
                if test_box_rect.colliderect(other_box):
                    valid_move = False

            if valid_move:
                box.x = new_box_x
                box.y = new_box_y

def can_push_box(box_index, dx, dy):
    box = boxes[box_index]
    new_box_x = box.x + dx * player_speed
    new_box_y = box.y + dy * player_speed
    test_box_rect = pygame.Rect(
        new_box_x - BOX_SIZE // 2,
        new_box_y - BOX_SIZE // 2,
        BOX_SIZE, BOX_SIZE
    )
    
    # Check if new position is valid
    for wall in walls:
        if test_box_rect.colliderect(wall):
            return False
    
    for other_box in boxes[:box_index] + boxes[box_index+1:]:
        if test_box_rect.colliderect(other_box):
            return False
    
    return True

def draw_game():
    screen.fill(BLACK)
    
    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, WHITE, wall)
    
    # Draw boxes
    for box in boxes:
        color = GREEN if is_on_target(box) else RED
        pygame.draw.rect(screen, color, box)
    
    # Draw targets
    for target in targets:
        pygame.draw.circle(screen, BLUE, (int(target[0]), int(target[1])), TARGET_RADIUS, 2)
    
    # Draw player
    pygame.draw.circle(
        screen, WHITE,
        (int(player_pos['x']), int(player_pos['y'])),
        PLAYER_RADIUS
    )

def is_on_target(box):
    for target in targets:
        if abs(box.x - target[0]) < BOX_SIZE // 2 and abs(box.y - target[1]) < BOX_SIZE // 2:
            return True
    return False

def check_win():
    for box in boxes:
        if not is_on_target(box):
            return False
    return True

running = True
won = False

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT or event.key == K_a:
                move_x = -1
            elif event.key == K_RIGHT or event.key == K_d:
                move_x = 1
            elif event.key == K_UP or event.key == K_w:
                move_y = -1
            elif event.key == K_DOWN or event.key == K_s:
                move_y = 1
        elif event.type == KEYUP:
            if event.key in [K_LEFT, K_RIGHT, K_a, K_d]:
                move_x = 0
            elif event.key in [K_UP, K_DOWN, K_w, K_s]:
                move_y = 0
    
    # Update player position
    move_player(move_x, move_y)
    
    # Draw game state
    draw_game()
    
    # Check win condition
    if not won and check_win():
        won = True
        font = pygame.font.Font(None, 36)
        text = font.render("You Win!", True, GREEN)
        screen.blit(text, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2))
    
    # Reset game on space press after win
    if won:
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            boxes.clear()
            for y in range(6):
                for x in range(8):
                    if level_layout[y][x] == 2:
                        box_rect = pygame.Rect(
                            x * CELL_SIZE - BOX_SIZE // 2 + CELL_SIZE % 2,
                            y * CELL_SIZE - BOX_SIZE // 2 + CELL_SIZE % 2,
                            BOX_SIZE, BOX_SIZE
                        )
                        boxes.append(box_rect)
            player_pos['x'] = 2 * CELL_SIZE
            player_pos['y'] = 2 * CELL_SIZE
            won = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
