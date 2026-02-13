import pygame
from math import radians, sin, cos, sqrt
from brain import Brain
import numpy as np

# Poprawione kąty (315 zamiast 305)
angles = (0, 30, 60, 90, 270, 300, 330)

walls = [((0, 50), (0, 100)),
    ((0, 50), (200, 50)),
    ((0, 100), (150, 100)),
    ((200, 50), (200, 350)),
    ((150, 100), (150, 400)),
    ((200, 350), (500, 350)),
    ((150, 400), (500, 400))
]

finish = (500, 375)

class Car(pygame.sprite.Sprite):
    def __init__(self, brain=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = 35
        self.y = 75
        self.frames_alive = 0
        self.last_x = self.x
        self.last_y = self.y
        self.rayLen = 50
        self.alive = True
        self.fitness = 0
        self.image = pygame.Surface([10, 10])
        self.image.fill("red")
        self.rect = self.image.get_rect()
        if brain == None:
            self.brain = Brain()
        else:
            self.brain = brain
        self.update()

    def update(self):
        self.check_collision(walls)
        if self.alive == False:
            return 0
        else:
            self.rays = []
            self.distances = []
            self.calculate_fitness(finish)
            for ang in angles:
                # Używamy standardowego cos dla X i sin dla Y
                end_x = self.x + self.rayLen * cos(radians(ang))
                end_y = self.y + self.rayLen * sin(radians(ang))
                self.rays.append([(self.x, self.y), (int(end_x), int(end_y))])
            
            self.rect.center = (self.x, self.y)
            self.calculate_intersection_point(walls)
            self.move(self.distances)
            self.frames_alive += 1

            # Co 60 klatek (1 sekunda) sprawdź, czy auto się ruszyło
            if self.frames_alive % 60 == 0:
                dist_moved = sqrt((self.x - self.last_x)**2 + (self.y - self.last_y)**2)
                if dist_moved < 5: # Jeśli przejechało mniej niż 5 pikseli w sekundę...
                    self.alive = False # ...to dowidzenia, giniesz za lenistwo
                
                # Zaktualizuj ostatnią pozycję do kolejnego sprawdzenia
                self.last_x = self.x
                self.last_y = self.y

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

    def check_collision(self, walls):
        for wall in walls:
            if self.rect.clipline(wall):
                self.alive = False

    def get_input_data(self):
        return self.distances
        
    def calculate_fitness(self, finish):
        dist = sqrt( (self.x - finish[0]) ** 2 + (self.y - finish[1]) ** 2)
        self.fitness = 1 / (1 + dist)

    def move(self, distances):
        predicted_move = np.argmax(self.brain.predict(distances))

        if predicted_move == 0:
            self.x += 1
        elif predicted_move == 1:
            self.y += 1
        elif predicted_move == 2:
            self.x -= 1
        else:
            self.y += 1

