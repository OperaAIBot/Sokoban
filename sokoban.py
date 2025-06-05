class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.on_target = False

def initialize_level(level):
    player = None
    boxes = []
    targets = []
    walls = []

    for y in range(len(level)):
        for x in range(len(level[y])):
            cell = level[y][x]
            if cell == '@':
                player = Player(x, y)
            elif cell == '.':
                targets.append((x, y))
            elif cell == '#':
                boxes.append(Box(x, y))

    walls = [(x, y) for y in range(len(level)) 
             for x in range(len(level[y])) if level[y][x] == 'W']
    
    return player, boxes, targets, walls

def is_win(boxes, targets):
    # Check if all boxes are on target positions
    for box in boxes:
        if (box.x, box.y) not in targets or not box.on_target:
            return False
    return True

def main():
    level = [
        "#########",
        "#@. .  #",
        "# ###   #",
        "# ## ####",
        "#  #     #",
        "#########"
    ]

    player, boxes, targets, walls = initialize_level(level)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_UP:
                    dy = -1
                elif event.key == pygame.K_DOWN:
                    dy = 1
                elif event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1

                new_x = player.x + dx
                new_y = player.y + dy

                # Check if the move is into a wall or outside the grid
                if (new_x, new_y) in walls or not (0 <= new_x < len(level[0])) or not (0 <= new_y < len(level)):
                    continue  # Can't move

                # Check if moving into a box
                moved_box = None
                for box in boxes:
                    if box.x == new_x and box.y == new_y:
                        moved_box = box
                        break

                if moved_box is not None:
                    box_new_x = moved_box.x + dx
                    box_new_y = moved_box.y + dy

                    # Check if the box can be moved (i.e., into an empty space or target)
                    if (box_new_x, box_new_y) in walls or (abs(dx) + abs(dy) != 1):
                        continue

                    for other_box in boxes:
                        if other_box == moved_box:
                            continue
                        if other_box.x == box_new_x and other_box.y == box_new_y:
                            # Box can't be pushed into another box
                            continue

                    # Update the box's position
                    moved_box.x += dx
                    moved_box.y += dy

                    # Check if it's on a target
                    if (moved_box.x, moved_box.y) in targets:
                        moved_box.on_target = True
                    else:
                        moved_box.on_target = False

                # Update player position
                player.x = new_x
                player.y = new_y

        # Clear the screen
        screen.fill(BLACK)

        # Draw walls
        for x, y in walls:
            pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw boxes
        for box in boxes:
            color = GREEN if box.on_target else RED
            pygame.draw.rect(screen, color, (box.x * CELL_SIZE, box.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if not box.on_target:
                pygame.draw.circle(screen, BLACK, (box.x * CELL_SIZE + 10, box.y * CELL_SIZE + 10), 3)

        # Draw targets
        for x, y in targets:
            pygame.draw.circle(screen, GREEN, (x * CELL_SIZE + 10, y * CELL_SIZE + 10), 8)

        # Draw player
        pygame.draw.rect(screen, BLUE, (player.x * CELL_SIZE, player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if is_win(boxes, targets):
            font = pygame.font.Font(None, 36)
            text = font.render("WIN", True, YELLOW)
            screen.blit(text, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 20))
            # Reset the game
            player, boxes, targets, walls = initialize_level(level)

        # Update display
        pygame.display.flip()

    pygame.quit()

# Initialize Pygame and run the main function
pygame.init()
CELL_SIZE = 20
SCREEN_WIDTH = 15 * CELL_SIZE
SCREEN_HEIGHT = 9 * CELL_SIZE
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban")

if __name__ == "__main__":
    main()
