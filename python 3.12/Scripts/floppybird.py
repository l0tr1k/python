import pygame
import random

# Inicializácia pygame
pygame.init()

# Nastavenie okna
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Floppy Bird")

# Farby
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Nastavenie hodín
clock = pygame.time.Clock()

# Nastavenie vtáčka
bird_width, bird_height = 40, 40
bird_x, bird_y = 100, height // 2
bird_velocity = 0
gravity = 0.5

# Nastavenie prekážok
obstacle_width = 70
obstacle_gap = 200
obstacle_velocity = 3
obstacles = []

# Skóre
score = 0
font = pygame.font.SysFont(None, 55)

def draw_bird(x, y):
    pygame.draw.rect(screen, blue, (x, y, bird_width, bird_height))

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, black, obstacle)

def move_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle.x -= obstacle_velocity
    return [obstacle for obstacle in obstacles if obstacle.x > -obstacle_width]

def add_obstacle(obstacles):
    gap_y = random.randint(100, height - 100 - obstacle_gap)
    top_obstacle = pygame.Rect(width, 0, obstacle_width, gap_y)
    bottom_obstacle = pygame.Rect(width, gap_y + obstacle_gap, obstacle_width, height - gap_y - obstacle_gap)
    obstacles.append(top_obstacle)
    obstacles.append(bottom_obstacle)

def check_collision(obstacles, bird_x, bird_y):
    for obstacle in obstacles:
        if obstacle.colliderect(pygame.Rect(bird_x, bird_y, bird_width, bird_height)):
            return True
    return False

# Hlavná slučka hry
running = True
while running:
    screen.fill(white)

    # Spracovanie udalostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -10

    # Pohyb vtáčka
    bird_velocity += gravity
    bird_y += bird_velocity

    # Pridávanie prekážok
    if len(obstacles) == 0 or obstacles[-1].x < width - 200:
        add_obstacle(obstacles)

    # Pohyb prekážok
    obstacles = move_obstacles(obstacles)

    # Kontrola kolízií
    if check_collision(obstacles, bird_x, bird_y) or bird_y > height or bird_y < 0:
        running = False

    # Kreslenie objektov
    draw_bird(bird_x, bird_y)
    draw_obstacles(obstacles)

    # Zobrazenie skóre
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    # Aktualizácia obrazovky
    pygame.display.update()

    # Zvyšovanie skóre
    for obstacle in obstacles:
        if obstacle.x + obstacle_width == bird_x:
            score += 0.5

    # Nastavenie FPS
    clock.tick(30)

# Ukončenie hry
pygame.quit()