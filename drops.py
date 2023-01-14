import pygame
from random import choice
from pygame.sprite import Sprite

class EnemyDrop(Sprite):
    def __init__(self, enemy, game):

        # Inherit from Sprite
        super().__init__()

        # Get settings
        self.game = game
        self.settings = game.settings

        # Initialize enemy variables
        self.enemy = enemy
        self.enemy_rect = enemy.rect
        


        # Randomize the possible drops
        self.random = choice(("increaseDmg", "increaseBulletSpeed", "increaseFireRate", "increasePlayerMovementSpeed"))
        self.random_result = self.random

        # Polymorphism according to result of randint

        if self.random_result == "increaseDmg": # Upgrade bullet damage (red)
            self.image = pygame.image.load("resources\Enemies\increaseDmg.png").convert_alpha()

        elif self.random_result == "increaseBulletSpeed": # Upgrade bullet speed (blue)
            self.image = pygame.image.load("resources\Enemies\increaseBulletSpeed.png").convert_alpha()

        elif self.random_result == "increaseFireRate": # Upgrade fire rate (yellow)
            self.image = pygame.image.load("resources\Enemies\increaseFireRate.png").convert_alpha()

        elif self.random_result == "increasePlayerMovementSpeed": # Upgrade player movement speed (cyan)
            self.image = pygame.image.load("resources\Enemies\increasePlayerMovementSpeed.png").convert_alpha()


        self.image = pygame.transform.rotozoom(self.image, 0, 0.4)
        self.rect = self.image.get_rect(center = self.enemy_rect.center)

        # Create a mask from self.image (for collisions)
        self.mask = pygame.mask.from_surface(self.image)

        # Create a tick to track lifetime
        self.timeSpawn = self.game.global_tick


    def destroy(self):
        self.timeNow = self.game.global_tick
        if self.timeNow - self.timeSpawn > self.settings.drops_lifetime:
            self.kill()

     

    def checkPlayerCollision(self, buff):
    
        if pygame.sprite.spritecollide(self, self.enemy.game.player, False, pygame.sprite.collide_mask):
            if buff == "increaseDmg":
                self.settings.pBullet_rawDamage *= 1.8
            
            elif buff == "increaseBulletSpeed":
                if self.settings.pBullet_speed <= 30:
                    self.settings.pBullet_speed *= 1.2

            elif buff == "increaseFireRate":
                if self.settings.pBullet_cooldown >= 100: #ms
                    self.settings.pBullet_cooldown /= 1.4
            
            elif buff == "increasePlayerMovementSpeed":
                if self.settings.player_speed <= 18:
                    self.settings.player_speed *= 1.05
            
            self.kill()
                

    def update(self):
        self.checkPlayerCollision(self.random_result)
        self.destroy()
