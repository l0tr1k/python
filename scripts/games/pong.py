#l0tr1k pong game
#version 1.0

import pygame
import sys

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCORE_COLOR = (200, 200, 200)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG - 2 Players")

# Game objects
left_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Ball movement
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

# Score
score_left = 0
score_right = 0
font = pygame.font.Font(None, 74)

def reset_ball():
    ball.center = (WIDTH//2, HEIGHT//2)
    global ball_speed_x, ball_speed_y
    ball_speed_y = BALL_SPEED
    ball_speed_x = -ball_speed_x

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Paddle movement
    keys = pygame.key.get_pressed()
    # Left paddle (W/S keys)
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    
    # Right paddle (UP/DOWN arrows)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collisions
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    
    # Paddle collisions
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1.05  # Increase speed slightly on each hit

    # Score points
    if ball.left <= 0:
        score_right += 1
        reset_ball()
    if ball.right >= WIDTH:
        score_left += 1
        reset_ball()

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Score display
    score_text_left = font.render(str(score_left), True, SCORE_COLOR)
    score_text_right = font.render(str(score_right), True, SCORE_COLOR)
    screen.blit(score_text_left, (WIDTH//4, 20))
    screen.blit(score_text_right, (3*WIDTH//4, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()