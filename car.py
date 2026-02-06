import pygame
from math import radians, sin, cos, sqrt

# Poprawione kąty (315 zamiast 305)
angles = (0, 45, 90, 135, 180, 225, 270, 315)

walls = [
    ((0, 50), (200, 50)),
    ((0, 100), (150, 100)),
    ((200, 50), (200, 350)),
    ((150, 100), (150, 400)),
    ((200, 350), (500, 350)),
    ((150, 400), (500, 400))
]

class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 35
        self.y = 75
        self.rayLen = 150 # Zwiększyłem trochę, żeby było lepiej widać

        self.image = pygame.Surface([10, 10])
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.update() # Od razu tworzy self.rays

    def update(self):
        # Promienie muszą być odświeżane co klatkę do pełnej długości
        self.rays = []
        self.distances = []
        for ang in angles:
            # Używamy standardowego cos dla X i sin dla Y
            end_x = self.x + self.rayLen * cos(radians(ang))
            end_y = self.y + self.rayLen * sin(radians(ang))
            self.rays.append([(self.x, self.y), (int(end_x), int(end_y))])
        
        self.rect.center = (self.x, self.y)

    def calculate_intersection_point(self, walls):
        for ray in self.rays:
            x1, y1 = ray[0]
            x2, y2 = ray[1]
            
            min_dist = float('inf')
            closest_point = None

            for wall in walls:
                x3, y3 = wall[0]
                x4, y4 = wall[1]

                denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if denom == 0: continue

                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
                u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom

                if 0 <= t <= 1 and 0 <= u <= 1:
                    px = x1 + t * (x2 - x1)
                    py = y1 + t * (y2 - y1)
                    dist = sqrt((x1 - px)**2 + (y1 - py)**2)
                    
                    if dist < min_dist:
                        min_dist = dist
                        closest_point = (int(px), int(py))

            if closest_point:
                ray[1] = closest_point
                self.distances.append(min_dist / self.rayLen) 
            else:
                self.distances.append(1)
        def get_input_data(self):
            return self.distances