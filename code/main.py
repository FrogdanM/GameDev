from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

from random import randint

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_images()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()


        self.setup()

        # gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        # Enemy timer
        self.enemy_cooldown = 500
        
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()

    def input(self):
    # mousebutton 1 - left click, 2 - middle, 3 - right, 4 - scroll up, 5 - scroll down
        if pygame.mouse.get_just_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            enemy_pos = self.gun.rect.center + self.gun.player_direction * 100

            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            print('Banana')
            
            Enemy(enemy_pos,(self.all_sprites, self.collision_sprites))
        # if pygame.mouse.get_just_pressed()[3] and self.can_shoot:
        #     print('Banana')
        #     enemy_pos = self.gun.rect.center + (1500, 0)
        #     Enemy(enemy_pos,(self.all_sprites, self.collision_sprites))
            
    
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True
    
    # ENEMY
    def enemy_spawn(self):
        Enemy(self.player.rect.center + 200,(self.all_sprites, self.collision_sprites))
    def enemy_timer(self):
        print(self.clock)
        if self.clock_time > 300 and pygame.mouse.get_just_pressed()[3]:
            Enemy(self.player.rect.center + 200,(self.all_sprites, self.collision_sprites))
            print('Banana')

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
        


    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() /1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # update
            

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)


            # update
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            pygame.display.flip()

            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()