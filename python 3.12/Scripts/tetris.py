import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock
clock = pygame.time.Clock()

# Grid
grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]

def draw_grid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    for y in range(len(grid)):
        pygame.draw.line(screen, WHITE, (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))
    for x in range(len(grid[0])):
        pygame.draw.line(screen, WHITE, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))

def new_piece():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    piece = {
        'shape': shape,
        'color': color,
        'x': SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2,
        'y': 0
    }
    return piece

def valid_space(piece, grid):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                if (piece['y'] + y >= len(grid) or
                    piece['x'] + x < 0 or piece['x'] + x >= len(grid[0]) or
                    grid[piece['y'] + y][piece['x'] + x] != BLACK):
                    return False
    return True

def place_piece(piece, grid):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                grid[piece['y'] + y][piece['x'] + x] = piece['color']

def clear_lines(grid):
    lines_cleared = 0
    for y in range(len(grid) - 1, -1, -1):
        if BLACK not in grid[y]:
            lines_cleared += 1
            del grid[y]
            grid.insert(0, [BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])
    return lines_cleared

def draw_piece(piece):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece['color'], ((piece['x'] + x) * BLOCK_SIZE, (piece['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def main():
    current_piece = new_piece()
    fall_time = 0
    fall_speed = 0.3
    running = True

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_piece(current_piece)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece['x'] -= 1
                    if not valid_space(current_piece, grid):
                        current_piece['x'] += 1
                if event.key == pygame.K_RIGHT:
                    current_piece['x'] += 1
                    if not valid_space(current_piece, grid):
                        current_piece['x'] -= 1
                if event.key == pygame.K_DOWN:
                    current_piece['y'] += 1
                    if not valid_space(current_piece, grid):
                        current_piece['y'] -= 1
                if event.key == pygame.K_UP:
                    # Rotate piece
                    rotated_piece = {
                        'shape': list(zip(*reversed(current_piece['shape']))),
                        'color': current_piece['color'],
                        'x': current_piece['x'],
                        'y': current_piece['y']
                    }
                    if valid_space(rotated_piece, grid):
                        current_piece['shape'] = rotated_piece['shape']

        # Auto fall
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece['y'] += 1
            if not valid_space(current_piece, grid):
                current_piece['y'] -= 1
                place_piece(current_piece, grid)
                lines_cleared = clear_lines(grid)
                if lines_cleared > 0:
                    print(f"Lines cleared: {lines_cleared}")
                current_piece = new_piece()
                if not valid_space(current_piece, grid):
                    print("Game Over!")
                    running = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()