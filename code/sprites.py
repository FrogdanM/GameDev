from pygame.sprite import Group
from settings import *
from math import atan2, degrees

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect  = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect  = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        
        #player connection

        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(0,1)

        # sprite setup
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        # gets a vector from the player to the mouse pos, normalize makes the x and why between -1 and 1 instead of 1200/720
        self.player_direction = (mouse_pos - player_pos).normalize()

        
    def rotate_gun(self):
        # atan2 gets a width and a height and returns an angle in radiants which will be converted into degrees
        # For gamedev u need trigonometry -> learn sin, cosin and tan
        # - 90 will make it rotate perpendicular to the player instead o paralel. Delete 90 too see what happens and then add it back
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        # if the image is on the left of the player it flips it on the y axis so it is not upside down
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)
    


    def update(self, _): 
        # it updates the position when the player position updates
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction  * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.direction = direction
        self.speed = 1200
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000 # 1 sec

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        self.pos = pos
        #self.load_images()
        self.state, self.frame_index = 'bat', 0
        self.image = pygame.image.load(join('images', 'enemies', 'bat', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = self.pos)

        super().__init__(groups)


        self.speed = 1200
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 500 # 0.5 sec

    def load_images(self):
        self.frames = {'bat':[],'blob':[],'skeleton':[]}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', 'enemies', state)):
                if file_names:
                    for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)
    
    def move(self):
        pass


    # def animate(self, dt):
    #     # get state
        
    #     # animate
    #     # if the character moves in any direction then play the anymation, else keep the last state and set the frame to 0
    #     if self.spawn_time - self.lifetime > 0:
    #         self.frame_index += 5 * dt # sets up the speed of the animaton
    #         self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
    #     else:
    #         self.image = self.frames[self.state][0]
    
    # def update(self, dt):
    #     self.move(dt)
    #     self.animate(dt)