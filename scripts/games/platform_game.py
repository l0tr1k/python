#l0tr1k platform game
#version 1.0

import pygame
from sys import exit
from pygame.math import Vector2

# Inicializácia
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Načítanie grafických assets
def import_sprite(path, size=(64,64)):
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for y in range(0, sheet.get_height(), size[1]):
        for x in range(0, sheet.get_width(), size[0]):
            frame = sheet.subsurface((x, y, size[0], size[1]))
            frames.append(pygame.transform.scale(frame, size))
    return frames

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = import_sprite('assets/player.png', size=(32,32))
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT-100))
        self.mask = pygame.mask.from_surface(self.image)
        
        # Pohyb
        self.direction = Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.8
        self.jump_force = -16
        self.on_ground = False

    def animate(self):
        if self.direction.x != 0 and self.on_ground:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
        else:
            self.frame_index = 0
        
        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.flip(self.image, self.direction.x < 0, False)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
            
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def jump(self):
        self.direction.y = self.jump_force
        self.on_ground = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def horizontal_collision(self, platforms):
        self.rect.x += self.direction.x * self.speed
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.direction.x < 0:
                    self.rect.left = platform.rect.right
                elif self.direction.x > 0:
                    self.rect.right = platform.rect.left

    def vertical_collision(self, platforms):
        self.apply_gravity()
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.direction.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.rect.top = platform.rect.bottom
                    self.direction.y = 0

    def update(self, platforms):
        self.input()
        self.horizontal_collision(platforms)
        self.vertical_collision(platforms)
        self.animate()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=200, height=40):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((94, 129, 162))
        self.rect = self.image.get_rect(topleft=(x, y))

# Herné objekty
player = Player()
platforms = pygame.sprite.Group(
    Platform(0, HEIGHT-40, WIDTH, 40),
    Platform(300, HEIGHT-150),
    Platform(500, HEIGHT-300),
    Platform(200, HEIGHT-400)
)

# Hlavný cyklus
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((143, 188, 219))
    platforms.draw(screen)
    
    player.update(platforms)
    screen.blit(player.image, player.rect)
    
    pygame.display.update()
    clock.tick(60)