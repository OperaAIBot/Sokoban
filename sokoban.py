import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 30
BOX_SIZE = 40
TARGET_SIZE = 25
WALL_THICKNESS = 20
SPEED = 5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = SPEED
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), int(PLAYER_SIZE/2))

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BOX_SIZE
        self.height = BOX_SIZE

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (int(self.x), int(self.y), BOX_SIZE, BOX_SIZE))

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TARGET_SIZE
        self.height = TARGET_SIZE

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), int(TARGET_SIZE/2))

class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (int(self.x), int(self.y), self.width, self.height))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban")
    clock = pygame.time.Clock()

    # Level setup
    level_layout = [
        "WWWWWWWWWWWWWWWW",
        "W....B..T....WW",
        "W....B..T....WW",
        "W...BBBB.T...WW",
        "W....B..T....WW",
        "W....B..T....WW",
        "WWWWWWWWWWWWWWWW"
    ]

    player = None
    boxes = []
    targets = []
    walls = []

    # Parse level layout
    for y, row in enumerate(level_layout):
        for x, char in enumerate(row):
            cell_x = x * (BOX_SIZE + 50)
            cell_y = y * (BOX_SIZE + 50) + 100

            if char == 'W':
                walls.append(Wall(cell_x - WALL_THICKNESS/2, cell_y - WALL_THICKNESS/2, WALL_THICKNESS, WALL_THICKNESS))
            elif char == 'P':
                player = Player(cell_x, cell_y)
            elif char == 'B':
                boxes.append(Box(cell_x + BOX_SIZE//2, cell_y + BOX_SIZE//2))
            elif char == 'T':
                targets.append(Target(cell_x + BOX_SIZE//2, cell_y + BOX_SIZE//2))

    def move(obj, dx=0, dy=0):
        obj.x += dx * obj.speed
        obj.y += dy * obj.speed

        # Check for collisions with walls and other objects
        if any(abs(obj.x - o.x) < (obj.width/2 + o.width/2) and abs(obj.y - o.y) < (obj.height/2 + o.height/2) for o in walls):
            obj.x -= dx * obj.speed
            obj.y -= dy * obj.speed
            return False

        if isinstance(obj, Player):
            for box in boxes:
                if abs(obj.x - box.x) < (PLAYER_SIZE/2 + BOX_SIZE/2) and abs(obj.y - box.y) < (PLAYER_SIZE/2 + BOX_SIZE/2):
                    if dx != 0 or dy != 0:
                        move(box, dx, dy)
                    obj.x -= dx * obj.speed
                    obj.y -= dy * obj.speed
                    return False

        return True

    running = True
    win = False

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if not win:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    move(player, -1, 0)
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    move(player, 1, 0)
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    move(player, 0, -1)
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    move(player, 0, 1)

        # Draw objects
        for wall in walls:
            wall.draw(screen)
        for target in targets:
            target.draw(screen)
        player.draw(screen)
        for box in boxes:
            box.draw(screen)

        # Check win condition
        if not win and set((box.x, box.y) for box in boxes).issuperset(set((target.x, target.y) for target in targets)):
            win = True

        if win:
            font = pygame.font.Font(None, 74)
            text = font.render("WIN", True, GREEN)
            screen.blit(text, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 37))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
