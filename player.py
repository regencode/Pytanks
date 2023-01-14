import pygame, sys

from pygame.sprite import Sprite
from pygame.math import Vector2

from bullet import *

class Player(Sprite):
    def __init__(self, game):

        # Inherit from Sprite
        super().__init__()

        # Initialize game variables for easy access
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.clock = game.clock


        # Initialize bullet group
        self.bullet_group = pygame.sprite.Group()

        # Fetch settings
        self.settings = game.settings

        # Initialize image and rect, downscale image
        self.image = pygame.image.load("resources\Player\playerTank.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.40)
        self.original_image = self.image

        #This rect will be moved around according to player input
        self.movement_rect = self.image.get_rect(center = self.screen_rect.center)

        #This rect will rotate freely based on angle to mouse cursor, but it will be anchored to the movement_rect
        self.rect = self.image.get_rect(center = self.movement_rect.center)

        # Movement flags
        self.moving_up = 0
        self.moving_down = 0
        self.moving_left = 0
        self.moving_right = 0

        # Rotation stats (for shooting bullets in the correct direction)
        self.angle = 0

        # Shooting flags, vars and sprites
        self.shootingBullets = False
        self.lastShotTick = self.game.global_tick

        #Setting health to max health
        self.health = self.settings.player_maxHealth

        self.level = 0
        self.exp = 0
        self.xpThresholds = self.settings.expThresholds

        # Initialize player-enemy collision timer
        self.collideLast = self.game.global_tick

        # Initialize boost tick (to track cooldown and length of boost)
        self.lastBoost = self.game.global_tick

    def stopGame(self):
        if self.health <= 0:
            self.game.game_active = 0
    
    def checkCollisions(self):
        self.collideTickNow = self.game.global_tick
        if pygame.sprite.spritecollide(self, self.game.enemy_group, False, pygame.sprite.collide_mask):
            if self.collideTickNow - self.collideLast >= self.settings.player_invulnerableTime:
                self.health -= self.settings.enemy_damage
                self.collideLast = self.collideTickNow
        
        elif pygame.sprite.spritecollide(self, self.game.enemyBullet_group, True, pygame.sprite.collide_mask):
            if self.collideTickNow - self.collideLast >= self.settings.player_invulnerableTime:
                self.health -= self.settings.eBullet_damage
                self.collideLast = self.collideTickNow
                

    def levelUp(self):
        if self.exp >= self.settings.expThresholds[self.level]:
            self.exp = 0
            self.level += 1

            # Restore health on level up by half
            self.health += self.settings.player_maxHealth*0.5
            if self.health > self.settings.player_maxHealth:
                self.health = self.settings.player_maxHealth


    def shootBullets(self, shooting):
        if shooting:
            self.currentRotation = -self.angle
            #Fire gun only after cooldown has elapsed

            #Get current tick when shooting is True
            self.shootNow = self.game.global_tick

            #If (current tick - last shot tick) has exceeded the cooldown defined in the settings
            if self.shootNow - self.lastShotTick >= self.settings.pBullet_cooldown:
                
                # Add bullet to the bullets sprite group
                self.bullet_group.add(PlayerBullet(self, self.game, self.currentRotation))

                # Export bullet group to main
                self.game.bullet_group = self.bullet_group

                # Set last tick to the value of current tick
                self.lastShotTick = self.shootNow
                

    def rotateSelf(self):
        # Get cursor position
        self.mouse_pos = pygame.mouse.get_pos()
        
        # Convert player position (as rect.center) to vector
        self.position = Vector2(self.rect.center)

        # Compute vector from center of player to cursor
        self.direction_vector = self.mouse_pos - self.position

        # Convert to polar coordinates to get distance and angle
        self.distanceToCursor, self.angle = self.direction_vector.as_polar()

        # Rotate the image using the original_image
        # Negative angle otherwise rotation goes the other way
        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        # Create new rect from the rotated image
        self.rect = self.image.get_rect(center = self.rect.center)

    def normalize_movement(self):
        # Init a 2d vector with the resultant values
        self.move_vector = Vector2(self.moving_right - self.moving_left, self.moving_down - self.moving_up)

        # to normalize diagonal movement
        if self.move_vector.x != 0 or self.move_vector.y != 0:
            self.move_vector.scale_to_length(self.settings.player_speed)
            self.rect.x += self.move_vector.x
            self.rect.y += self.move_vector.y


    def player_input(self):

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        if keys[pygame.K_w]:
            self.moving_up = 1
        else: self.moving_up = 0    

        if keys[pygame.K_s]:
            self.moving_down = 1
        else: self.moving_down = 0    

        if keys[pygame.K_a]:
            self.moving_left = 1
        else: self.moving_left = 0   

        if keys[pygame.K_d]:
            self.moving_right = 1
        else: self.moving_right = 0


        # Shoot using left mouse button 
        if mouse[0]:
            self.shootingBullets = True
        else:
            self.shootingBullets = False

    

    def update(self):

        # Player input
        self.player_input()

        # Movement 
        self.normalize_movement()

        # Rotation
        self.rotateSelf()

        # Shoot bullets (bullets updated in main)
        self.shootBullets(self.shootingBullets)

        # Check collisions with enemy and enemy bullets
        self.checkCollisions()

        #Update the level when the threshold is met/exceeded
        self.levelUp()

        # IMPORTANT - Pass the coordinates of player_rect to the game
        # for enemy AI
        self.game.player_rect = self.rect

        self.stopGame()

        
