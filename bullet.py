import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2

class Bullet(Sprite):
    def __init__(self, source, game, direction, speed, lifetime):

        # Source refers to the object that fires this bullet

        # Inherit from Sprite
        super().__init__()

        # Create game variables for easy access
        self.game = game
        self.screen = game.screen

        # Get the player variables to call source methods on source from this object
        self.source = source
        self.source_rect = self.source.rect

        # Place the bullet rect in the center of source rect
        self.rect = self.image.get_rect(center = self.source_rect.center)

        # Get the rotation of source, and use that to determine the direction of bullet travel
        self.direction = direction

        # Get bullet speed
        self.speed = speed

        # Get bullet lifetime
        self.lifetime = lifetime
        
        # Create a mask to detect pixel-perfect collisions
        self.mask = pygame.mask.from_surface(self.image)

        # Initialize tick variable to track bullet lifetime (and delete the bullet if it exceeds the lifetime)
        self.timeSpawn = self.game.global_tick

        # Initialize vector for bullet movement
        self.bulletTravelDirection = Vector2()

    def move(self):
        self.bulletTravelDirection.from_polar((self.speed, -self.direction+2)) #Offset by +2
        self.rect.x += self.bulletTravelDirection[0]
        self.rect.y += self.bulletTravelDirection[1]
        
    def destroy(self):
        # If the age of this bullet sprite exceeds the bullet lifetime defined in the settings, delete this bullet
        self.age = self.game.global_tick
        if self.age - self.timeSpawn >= self.lifetime:
            self.kill()

class PlayerBullet(Bullet):
    def __init__(self, player, game, playerRotation):

        #Load settings
        self.settings = game.settings
        self.speed = self.settings.pBullet_speed
        self.lifetime = self.settings.pBullet_lifetime

        # Load the image
        self.image = pygame.image.load('resources\Bullet\playerBullet.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, self.settings.pBullet_size)

        super().__init__(player, game, playerRotation, self.speed, self.lifetime)

        
    def update(self):
        # Update the mask
        self.mask = pygame.mask.from_surface(self.image)

        self.destroy()
        self.move()




class EnemyBullet(Bullet):
    def __init__(self, enemy, game, enemyRotation):

        #Load settings
        self.settings = game.settings
        self.eBullet_speed = self.settings.eBullet_speed
        self.lifetime = self.settings.eBullet_lifetime
        self.direction = enemyRotation

        # Load the image
        self.image = pygame.image.load('resources\Enemies\enemyBullet.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, self.settings.eBullet_size)
        
        super().__init__(enemy, game, self.direction, self.eBullet_speed, self.lifetime)

        
    def update(self):
        # Update the mask
        self.mask = pygame.mask.from_surface(self.image)

        self.destroy()
        self.move()
