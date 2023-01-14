import pygame
from pygame.sprite import Sprite

class Cursor(Sprite):
    def __init__(self, game):
        super().__init__()

        # Initialize game variables
        self.game = game
        self.screen = game.screen

        # Hide mouse
        pygame.mouse.set_visible(False)

        # Initialize image and rect
        self.image = pygame.image.load('resources\Game\game_crosshair.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.1)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()