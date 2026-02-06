import pygame

class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 10
        self.y = 75

        self.image = pygame.Surface([5, 5])
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)