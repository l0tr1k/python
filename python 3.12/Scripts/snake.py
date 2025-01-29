import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake block size
BLOCK_SIZE = 20

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Font for displaying score and level
font = pygame.font.SysFont(None, 35)

def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def display_score_and_level(score, level):
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, [10, 10])
    screen.blit(level_text, [SCREEN_WIDTH - 150, 10])

def game_loop():
    game_over = False
    game_close = False

    # Initial position of the snake
    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2

    # Change in position
    x_change = 0
    y_change = 0

    # Snake body
    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    # Initial speed and level
    speed = 10
    level = 1
    score = 0

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            game_over_text = font.render("Game Over! Press Q-Quit or C-Play Again", True, WHITE)
            screen.blit(game_over_text, [SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3])
            display_score_and_level(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # Check if snake hits the wall
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Add new head of the snake
        snake_head = [x, y]
        snake_list.append(snake_head)

        # Remove the tail if the snake is not growing
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake collides with itself
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_list)
        display_score_and_level(score, level)

        pygame.display.update()

        # Check if snake eats the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1
            score += 1

            # Increase level and speed every 5 points
            if score % 5 == 0:
                level += 1
                speed += 2  # Increase speed by 2 units

        clock.tick(speed)

    pygame.quit()
    quit()

# Start the game
game_loop()