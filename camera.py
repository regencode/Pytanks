import pygame
from pygame.sprite import Sprite

from world import GameWorld
from tiles import *



class Camera(Sprite):
    # Centered Player Camera

    def __init__(self, game):
        super().__init__()

        # Initialize game variables
        self.game = game
        self.screen = game.screen

        # Camera offset
        self.offset = pygame.math.Vector2(0, 0)
        
        # Player centering
        self.half_width = self.screen.get_size()[0] // 2
        self.half_height = self.screen.get_size()[1] // 2
        

        # Get ground
        self.ground_tile = GroundTile((0,0)) # Just for get_size
        self.ground_tile_sizeX = self.ground_tile.image.get_size()[0]
        self.ground_tile_sizeY = self.ground_tile.image.get_size()[1]
        self.ground_tile_group = pygame.sprite.Group()

        # Get world
        self.world = GameWorld()
        
        self.create_map()

    def create_map(self):
        for y in range(0, len(self.world.map_layout)):
            for x in range(0, len(self.world.map_layout[y])):
                #Negative values in order to place the player (2500, 1625) pixels from top left of the map, somewhere in the middle
                pos_x = x * self.ground_tile_sizeX - 2000
                pos_y = y * self.ground_tile_sizeY - 1300
                
                if self.world.map_layout[y][x] == "w": # walls of the game space
                    self.ground_tile_group.add(WallTile( (pos_x, pos_y)  ))

                else:
                    self.ground_tile_group.add(GroundTile( (pos_x, pos_y) ))



    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height


    def custom_draw(self):
        # note - offset is applied negative because it goes in the opposite direction of player movement

        # Draw the ground
        for tile in self.ground_tile_group:
            tile.rect.topleft = tile.rect.topleft - self.offset
            self.screen.blit(tile.image, tile.rect)
            
        # Draw other onscreen sprites
        # Apply camera offset to sprite positions before blit

        # Bullets

        for bullet in self.game.enemyBullet_group:
            bullet.rect.topleft = bullet.rect.topleft - self.offset
            self.screen.blit(bullet.image, bullet.rect)

        for bullet in self.game.bullet_group:
            bullet.rect.topleft = bullet.rect.topleft - self.offset
            self.screen.blit(bullet.image, bullet.rect)

        # Draw enemy drops
        for sprite in self.game.enemy_drops:
            sprite.rect.topleft = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, sprite.rect)

        # Player
        self.player = self.game.player

        self.center_target_camera(self.player.sprite)

        self.player.sprite.rect.topleft = self.player.sprite.rect.topleft - self.offset
        self.screen.blit(self.player.sprite.image, self.player.sprite.rect)


        # Enemies
        for sprite in self.game.enemy_group:
            sprite.rect.topleft = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, sprite.rect)


        # Draw the healthbar, with conditions
            sprite.health_bar.draw_with_condition()


        # Update cursor
        self.game.cursor.update()
