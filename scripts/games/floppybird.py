# l0tr1k flopy bird game
# version 1.0

import pygame
import random

# Init pygame
pygame.init()

# Window size
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Floppy Bird")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Time clock
clock = pygame.time.Clock()

# Bird setup
bird_width, bird_height = 40, 40
bird_x, bird_y = 100, height // 2
bird_velocity = 0
gravity = 0.5

# Obstacles setup
obstacle_width = 70
obstacle_gap = 300
obstacle_velocity = 3
obstacles = []

# Score
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

# Main loop
running = True
while running:
    screen.fill(white)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -10

    # Bird movement
    bird_velocity += gravity
    bird_y += bird_velocity

    # Add obstacles
    if len(obstacles) == 0 or obstacles[-1].x < width - 200:
        add_obstacle(obstacles)

    # Move obstacles
    obstacles = move_obstacles(obstacles)

    # Crash detection
    if check_collision(obstacles, bird_x, bird_y) or bird_y > height or bird_y < 0:
        running = False

    # Draw objects
    draw_bird(bird_x, bird_y)
    draw_obstacles(obstacles)

    # Print score
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    # Screen refresh
    pygame.display.update()

    # Score count when bird passes obstacle
   # Score tracking
    for obstacle in obstacles:  
        if obstacle.x < bird_x < obstacle.x + obstacle_width:
            score += 1

    # Timer setup FPS
    clock.tick(30)

# Game Over print
game_over_text = font.render("Game Over!", True, black)
screen.blit(game_over_text, (50, height // 2))
pygame.display.update() 

#Quit game
pygame.time.delay(1000)
pygame.quit()