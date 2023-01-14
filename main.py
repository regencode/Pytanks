import pygame, sys, os

from pygame.locals import *
from random import randint
from random import choice

from settings import Settings
from gui import *
from cursor import Cursor
from player import Player
from camera import Camera
from enemy import *


class Pytanks:

    # Spawn Manager, Sprite Updater, UI Drawer

    def __init__(self):

        # Initialize pygame
        pygame.init()
        self.global_tick = pygame.time.get_ticks()

        # Import Settings, clock
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Initialize screen and display flags
        self.display_flags = DOUBLEBUF
        self.screen = pygame.display.set_mode(self.settings.display_size, self.display_flags, 16)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Pytanks")
        self.screen.fill("Black")

        # Initialize game background
        self.bg = pygame.image.load('resources\Game\game_bg.PNG').convert()
        self.bg_width, self.bg_height = pygame.Surface.get_size(self.bg)

        # Initialize Cursor
        self.cursor = pygame.sprite.GroupSingle()
        self.cursor.add(Cursor(self))


        # Initialize Player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(self))
        self.player_rect = [0, 0]
        self.delayedPlayerCenterXY = [0, 0]

        # Initialize Enemy drops on death
        self.enemy_drops = pygame.sprite.Group()
        
        # Initialize Camera
        # We will use this object to draw most of the sprites on screen
        self.camera = Camera(self)

        # Initialize Enemy group
        self.enemy_group = pygame.sprite.Group()

        # Initialize Bullets (data to be received from Player sprite)
        self.bullet_group = pygame.sprite.Group()
        self.enemyBullet_group = pygame.sprite.Group()

        # USEREVENT - Spawn enemies with a cooldown
        self.spawn_enemy = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_enemy, randint(self.settings.enemy_spawnRateMin, self.settings.enemy_spawnRateMax))

        # USEREVENT - Get delayed player position (for enemy AI)
        self.delay_pos = pygame.USEREVENT + 2
        pygame.time.set_timer(self.delay_pos, randint(self.settings.player_posDelayMin, self.settings.player_posDelayMax))

        # USEREVENT = Increase difficulty by time
        self.increase_difficulty = pygame.USEREVENT + 3
        pygame.time.set_timer(self.increase_difficulty, 50000)

        # Initialize GUI
        self.gui = GUI(self)

        # Create a variable to show that the game is active/not active
        self.game_active = 1


    def run_game(self):    
        while self.game_active:

            self.global_tick = pygame.time.get_ticks()
            # Check for events
            self.checkEvents()

            # The sprites that are drawn last are on top
            self.camera.custom_draw()

            # Update all sprites, draw bullets shot by Player sprite
            self.updateAll()

            # Draw GUI and cursor
            self.drawSprites()
        
            self.clock.tick(self.settings.framerate)
            pygame.display.update()
        


    def checkEvents(self):
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If the player clicks on the x window button, exit the program
                sys.exit()

            if event.type == self.spawn_enemy:
                # Spawn enemy after a delay
                self.createEnemy()
            
            if event.type == self.delay_pos:
                # Update the player pos with a little bit of delay(for enemy AI)
                self.delayedPlayerCenterXY = self.player_rect.center
            
            if event.type == self.increase_difficulty:
                # Increase the difficulty after a defined period of time
                self.settings.update_difficulty()


    def createEnemy(self):
        # Append a new Enemy to the enemies Group if current enemy num is less than the max num
        if len(self.enemy_group) < self.settings.enemy_maxNum:

            # As the time goes up, the spawn pool changes to favor spawning the rectangle enemies more.
            if self.global_tick <= 30000:
                self.enemy_group.add(choice( (Triangle(self),Triangle(self),Triangle(self), Triangle(self), Triangle(self)) ))

            elif self.global_tick >= 30000:
                self.enemy_group.add(choice( (Triangle(self),Triangle(self),Triangle(self), Triangle(self), Rectangle(self)) ))          

            elif self.global_tick >= 80000:
                self.enemy_group.add(choice( (Triangle(self),Triangle(self),Triangle(self), Rectangle(self), Rectangle(self)) ))        

            elif self.global_tick >= 150000:
                self.enemy_group.add(choice( (Triangle(self),Triangle(self),Rectangle(self), Rectangle(self), Rectangle(self)) ))          

               

    def updateAll(self):
        
        # Update all the sprites
        self.enemy_drops.update()
        self.player.update()
        self.enemy_group.update()
        self.gui.update()
        self.enemyBullet_group.update()
        self.bullet_group.update()
    
    def drawSprites(self):
        
        # Update and draw GUI and Cursor (other sprites are drawn using the camera)
        
        self.gui.custom_draw()
        self.cursor.draw(self.screen)

if __name__ == "__main__":
    pt_game = Pytanks()
    pt_game.run_game()