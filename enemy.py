import pygame

from pygame.sprite import Sprite
from pygame.math import Vector2
from random import randint
from random import choice

from healthbar import HealthBar
from drops import EnemyDrop
from bullet import EnemyBullet

class Enemy(Sprite):
    def __init__(self, game):

        # Inherit from Sprite
        super().__init__()

        # Initialize game variables for easy access
        self.game = game
        self.screen = game.screen
        self.player = game.player.sprite
        self.screen_rect = game.screen_rect
        self.settings = self.game.settings

        # Create an original image variable in order to update the sprite image with rotations later on
        self.original_image = self.image

        # Create rect and place it offscreen
        self.rect = self.image.get_rect( center = choice((self.screen_rect.topleft, self.screen_rect.midtop, self.screen_rect.topright, self.screen_rect.midleft, self.screen_rect.midright, self.screen_rect.bottomright, self.screen_rect.midbottom, self.screen_rect.bottomleft)))


        # Create a mask to detect pixel-perfect collisions
        self.mask = pygame.mask.from_surface(self.image)


        # Initialize distance to player var
        self.distanceXY = [0, 0]

        # Initialize velocity and acceleration values
        self.velocity = Vector2()
        self.accel_x = 0
        self.accel_y = 0

        # Initialize normalized direction
        self.distance_normalize = 0

        # Initialize Health Bar
        self.health_bar = HealthBar(self)


    def dropItemOnDeath(self):
        randomizer = randint(0, 2)
        if randomizer == 1: # 33% chance to drop an item on kill that increases player stats

            # Add the enemy drop to the enemy_drop group in main
            self.game.enemy_drops.add(EnemyDrop(self, self.game))


    def destroyZeroHP(self):
        if self.current_health <= 0:
            self.dropItemOnDeath()
            self.kill()
            self.game.gui.updateScore()
            self.player.exp += self.settings.enemy_expOnKill


    def checkCollisions(self):
        if pygame.sprite.spritecollide(self, self.game.bullet_group, True, pygame.sprite.collide_mask):
            self.current_health -= self.settings.pBullet_damage


    def accelerate(self, accelX, accelY):
        # Acceleration based movement
        self.velocity[0] += accelX
        self.velocity[1] += accelY
        self.maxSpeed = self.settings.enemy_maxSpeed

        
        # Implement max positive velocity
        if self.velocity[0] >= 0:
            if self.velocity[0] >= self.maxSpeed:
                self.velocity[0] = self.maxSpeed

        # Implement "max" negative velocity
        else:
            if self.velocity[0] <= -self.maxSpeed:
                self.velocity[0] = -self.maxSpeed

        if self.velocity[1] >= 0:
            if self.velocity[1] >= self.maxSpeed:
                self.velocity[1] = self.maxSpeed
        else:
            if self.velocity[1] <= -self.maxSpeed:
                self.velocity[1] = -self.maxSpeed
        
        # Move the enemy movement rect
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def moveTowards(self, distance):
        # Extremely simple enemy AI movement
        self.accelThreshold = self.settings.enemy_accelThreshold

        try:
            self.distance_normalize = Vector2.normalize(distance)
        except ValueError: self.distance_normalize = [1, 1]

        
        self.accel_x = self.distance_normalize[0] * self.accelThreshold
        self.accel_y = self.distance_normalize[1] * self.accelThreshold
        self.accelerate(self.accel_x, self.accel_y)

    def rotateSelf(self):
        # Rotate facing player
        self.rotationAngle = self.distanceXY.as_polar()[1]
        self.image = pygame.transform.rotozoom(self.original_image, -self.rotationAngle, 1)

    def getTravelDirection(self):
        # Fetch the player_rect_center from the game
        self.player_rect_center = self.game.delayedPlayerCenterXY

        # Create a vector that describes the x and y distance to player
        self.distanceXY = Vector2((self.player_rect_center[0] - self.rect.centerx, self.player_rect_center[1] - self.rect.centery))
    

class Triangle(Enemy):
    def __init__(self, game):

        self.game = game
        self.settings = game.settings


        # Import image
        self.image = pygame.image.load('resources\Enemies\enemyTriangle.png').convert_alpha()

        # Initialize health point values
        self.max_health = self.settings.enemy_maxHealth
        self.current_health = self.max_health

        # Inherit from Enemy
        super().__init__(game)


    def update(self):
        # Update the mask
        self.mask = pygame.mask.from_surface(self.image)

        # Get direction of travel, move towards that direction and rotate self according to direction
        self.getTravelDirection()
        self.moveTowards(self.distanceXY)
        self.rotateSelf()

        # Check collisions with player bullets. Destroy self after its HP reaches 0 or below
        self.checkCollisions()
        self.destroyZeroHP()



class Rectangle(Enemy):
    def __init__(self, game):
        
        self.game = game
        self.settings = game.settings


        # Initialize health point values
        self.max_health = self.settings.rectangle_maxHealth
        self.current_health = self.max_health
        
        # Import image
        self.image = pygame.image.load('resources\Enemies\enemyRectangle.png').convert_alpha()

        # Inherit from Enemy
        super().__init__(game)
        self.lastShotTick = self.game.global_tick

    
    def shootBullets(self):
        
        #Fire gun only after cooldown has elapsed
        #Get current tick when shooting is True
        self.shootNow = self.game.global_tick

        #If (current tick - last shot tick) has exceeded the cooldown defined in the settings
        if self.shootNow - self.lastShotTick >= self.settings.eBullet_cooldown:
            
            # Add bullet to the bullets sprite group
            self.game.enemyBullet_group.add(EnemyBullet(self, self.game, -self.rotationAngle))

            # Set last tick to the value of current tick
            self.lastShotTick = self.shootNow


    def update(self):
        # Update the mask
        self.mask = pygame.mask.from_surface(self.image)

        # Get direction of travel, move towards that direction and rotate self according to direction
        self.getTravelDirection()
        self.moveTowards(self.distanceXY)
        self.rotateSelf()

        # Rectangle exclusive (shoot bullets)
        # Shoot bullets and update it
        self.shootBullets()

        # Check collisions with player bullets. Destroy self after its HP reaches 0 or below
        self.checkCollisions()
        self.destroyZeroHP()
