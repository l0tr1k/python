import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH // 2 - 10, HEIGHT - 40, 20, 20)
bullets = []
asteroids = []
lives = 3
score = 0
level = 1
asteroid_speed = 2
asteroid_spawn_rate = 2000
running = True

font = pygame.font.Font(None, 36)
last_spawn = pygame.time.get_ticks()

def spawn_asteroid():
    asteroids.append(pygame.Rect(random.randint(0, WIDTH - 30), 0, 30, 30))

def move_objects():
    global score, level, asteroid_speed, running
    for bullet in bullets[:]:
        bullet.y -= 5
        if bullet.y < 0:
            bullets.remove(bullet)
    
    for asteroid in asteroids[:]:
        asteroid.y += asteroid_speed
        if asteroid.y > HEIGHT:
            running = False  # Game over if asteroid reaches bottom
        for bullet in bullets[:]:
            if asteroid.colliderect(bullet):
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                score += 10
                if score % 50 == 0:
                    level += 1
                    asteroid_speed += 1

while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x -= 20
            if event.key == pygame.K_RIGHT:
                player.x += 20
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player.x + 8, player.y, 5, 10))
            if event.key == pygame.K_ESCAPE:
                running = False  # Exit game on ESC
    
    move_objects()
    
    if pygame.time.get_ticks() - last_spawn > asteroid_spawn_rate:
        spawn_asteroid()
        last_spawn = pygame.time.get_ticks()
    
    pygame.draw.rect(screen, (255, 255, 255), player)
    for bullet in bullets:
        pygame.draw.rect(screen, (0, 0, 255), bullet)
    for asteroid in asteroids:
        pygame.draw.rect(screen, (128, 128, 128), asteroid)
    
    score_text = font.render(f"Score: {score} Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
