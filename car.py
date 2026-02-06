import pygame
from math import radians, sin, cos

angles = (0, 45, 90, 135, 180, 225, 270, 305)

class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 35
        self.y = 75
        self.rayLen = 20

        self.image = pygame.Surface([5, 5])
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rays = [((self.x, self.y), (int(self.x + self.rayLen * sin(radians(ang))), int(self.y + self.rayLen * cos(radians(ang))))) for ang in angles]
        self.rect.center = (self.x, self.y)