import pygame
from math import radians, sin, cos, sqrt
from brain import Brain
import numpy as np
import random

# Poprawione kąty (315 zamiast 305)
angles = (0, 30, 60, 90, 270, 300, 330)

walls = [
    ((0, 50), (0, 150)),      # Ściana startowa (lewa) - teraz ma 100px wysokości
    ((0, 50), (250, 50)),     # Górna krawędź pierwszego odcinka (wydłużona do 250)
    ((0, 150), (150, 150)),   # Dolna krawędź pierwszego odcinka (szerokość 100)
    
    ((250, 50), (250, 350)),  # Prawa krawędź pionowego odcinka
    ((150, 150), (150, 450)), # Lewa krawędź pionowego odcinka (szerokość 100)
    
    ((250, 350), (500, 350)), # Górna krawędź ostatniego odcinka
    ((150, 450), (500, 450))  # Dolna krawędź ostatniego odcinka (szerokość 100)
]

checkpoints = [
    ((100, 50), (100, 150)),   # 1. Połowa pierwszej prostej   # 2. Przed pierwszym zakrętem
    ((250, 200), (150, 200)),
    ((250, 300), (150, 300)),  # 4. Przed drugim zakrętem
    ((250, 350), (220, 450)),
    ((400, 350), (400, 450))  # 5. Na ostatniej prostej
]

# Pamiętaj, aby zaktualizować też metę, by była na środku nowej drogi:
finish = (500, 350)

class Car(pygame.sprite.Sprite):
    def __init__(self, brain=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = 45
        self.y = 100
        self.angle = 0
        self.speed = 0
        self.maxspeed = 6
        self.frames_alive = 0
        self.last_x = self.x
        self.last_y = self.y
        self.rayLen = 150
        self.alive = True
        self.fitness = 0
        self.original_image = pygame.Surface([40, 20], pygame.SRCALPHA)
        self.original_image.fill("red")
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.passed_checkpoints = []
        self.checkpoint_score = 0

        if brain == None:
            self.brain = Brain()
        else:
            self.brain = brain
        self.update()

    def update(self):
        self.check_collision(walls, checkpoints)
        if self.alive == False:
            return 0
        else:
            self.rays = []
            self.distances = []
            self.calculate_fitness(finish)
            for ang in angles:
                
                end_x = self.x + self.rayLen * cos(radians(ang + self.angle) )
                end_y = self.y + self.rayLen * sin(radians(ang + self.angle))
                self.rays.append([(self.x, self.y), (int(end_x), int(end_y))])

            self.calculate_intersection_point(walls)
            self.move(self.distances)
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=(self.x, self.y))
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

    def check_collision(self, walls, checkpoints):
        for wall in walls:
            if self.rect.clipline(wall):
                self.alive = False
        for i in range(len(checkpoints)):
            if i not in self.passed_checkpoints and self.rect.clipline(checkpoints[i]):
                self.passed_checkpoints.append(i)
                if i == 3:
                    self.checkpoint_score += 500
                else:
                    self.checkpoint_score += 100


    def get_input_data(self):
        return self.distances
        
    def calculate_fitness(self, finish):
        dist = sqrt((self.x - finish[0])**2 + (self.y - finish[1])**2)
        self.fitness = self.checkpoint_score + (100 / (1 + dist))

    def move(self, distances):
        predicted_move = np.argmax(self.brain.predict(distances))

        if predicted_move == 0:
            if self.speed > 0:
                self.angle += 2
        elif predicted_move == 1:
            if self.speed > 0:
                self.angle -= 2
        elif predicted_move == 2:
            self.speed = min(self.speed + 0.01, self.maxspeed)
        else:
            self.speed = max(self.speed - 0.01, 0)
        a, b = self.speed * cos(radians(self.angle)), self.speed * sin(radians(self.angle))
        self.x += a
        self.y += b


            

print(random.sample(range(0,10), 2))