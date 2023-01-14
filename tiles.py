import pygame
from pygame.sprite import Sprite

class GroundTile(Sprite):
    def __init__(self, pos):

        # Inherit from sprite
        super().__init__()

        self.image = pygame.image.load("resources\Game\game_bg.PNG").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class WallTile(Sprite):
    def __init__(self, pos):

        # Inherit from sprite
        super().__init__()

        self.image = pygame.image.load("resources\Game\wall_bg.PNG").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos