from typing import Any
import pygame
from os.path import join

pygame.init()

# setup
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Vampire survivor")
running = True
clock = pygame.time.Clock()



class Player(pygame.sprite.Sprite):
    def __init__(self, frames, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.arrow_pressed = 0
        self.image = self.frames[0][self.frame_index]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300
    

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            if int(keys[pygame.K_LEFT]):
                self.frame_index += 5 * dt
                self.arrow_pressed = 2
                if self.frame_index < len(self.frames):
                    self.image = self.frames[self.arrow_pressed][int(self.frame_index)]
                else:
                    self.frame_index = 0
                    self.direction.x = 0
                    self.direction.y = 0
            if int(keys[pygame.K_RIGHT]):
                self.frame_index += 5 * dt
                self.arrow_pressed = 3
                if self.frame_index < len(self.frames):
                    self.image = self.frames[self.arrow_pressed][int(self.frame_index)]
                else:
                    self.frame_index = 0
                    self.direction.x = 0
                    self.direction.y = 0

        elif keys[pygame.K_DOWN] or keys[pygame.K_UP]:
            self.direction.y = int(keys[pygame.K_DOWN])- int(keys[pygame.K_UP])
            if int(keys[pygame.K_DOWN]):
                self.frame_index += 5 * dt
                self.arrow_pressed = 0
                if self.frame_index < len(self.frames):
                    self.image = self.frames[self.arrow_pressed][int(self.frame_index)]
                else:
                    self.frame_index = 0
                    self.direction.x = 0
                    self.direction.y = 0

            if int(keys[pygame.K_UP]):
                self.frame_index += 5 * dt
                self.arrow_pressed = 1
                if self.frame_index < len(self.frames):
                    self.image = self.frames[self.arrow_pressed][int(self.frame_index)]
                else:
                    self.frame_index = 0
                    self.direction.x = 0
                    self.direction.y = 0
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.image = self.frames[self.arrow_pressed][0]

        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt



# # imports

move_down = [pygame.image.load(join('images', 'player', 'down', f'{i}.png')).convert_alpha() for i in range (4)]
move_left = [pygame.image.load(join('images', 'player', 'left', f'{i}.png')).convert_alpha() for i in range (4)]
move_right = [pygame.image.load(join('images', 'player', 'right', f'{i}.png')).convert_alpha() for i in range (4)]
move_up = [pygame.image.load(join('images', 'player', 'up', f'{i}.png')).convert_alpha() for i in range (4)]
movement = [move_down, move_up, move_left, move_right]
# class Animated_walk(pygame.sprite.Sprite):
#     def __init__(self, frames, pos, groups):
#         super().__init__(groups)
#         self.frames = frames
#         self.frame_index = 0
#         self.image = self.frames[self.frame_index]
#         self.rect = self.image.get_frect(center = pos)
    
#     def update(self, dt):
#         self.frame_index += 5 * dt
#         if self.frame_index < len(self.frames):
#             self.image = self.frames[int(self.frame_index)]
#         else:
#             self.kill()
        

# sprites

all_sprites = pygame.sprite.Group()
player = Player(movement, all_sprites)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    dt = clock.tick(100) / 1000
    all_sprites.update(dt) 

    display_surface.fill('#3a2e3f')
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
