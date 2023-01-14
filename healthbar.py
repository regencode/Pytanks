import pygame

class HealthBar:
    def __init__(self, sprite):

        # initialize sprite variables
        self.sprite = sprite
        self.sprite_rect = sprite.rect
        self.max_health = self.sprite.max_health
        self.current_health = self.sprite.current_health

    
    def draw(self):
        self.healthbarcontainer = pygame.draw.rect(self.sprite.screen, "Grey", ((self.sprite_rect.centerx-10, self.sprite_rect.centery+80), (80, 8)))

        if self.current_health < self.max_health:
        # Get the width of green healthbar
    
            self.bar_width = 80*((self.current_health/self.max_health))//1
            # floor division by 1 to round it to an int

            # Draw the image
            self.image = pygame.draw.rect(self.sprite.screen, "Green", ((self.sprite_rect.centerx-10, self.sprite_rect.centery+80), (self.bar_width, 5)))

    def draw_with_condition(self):
        self.current_health = self.sprite.current_health
        if self.current_health < self.max_health:
            self.draw()
