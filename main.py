import pygame
from pygame.locals import *
from car import Car, walls, finish
from brain import Brain
import numpy as np
#POLICZYĆ GDZIE PRZECINA SIĘ KAŻDY PROMIEŃ

POP_SIZE = 50
GENERATIONS = 10

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    temp_car = Car()
    pygame.display.set_caption('Basic Pygame program')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)
    clock = pygame.time.Clock()
    end = pygame.Surface([10, 50])
    end.fill("purple")
    endrect = end.get_rect()
    endrect.center = finish
    generation = 1
    

    cars = pygame.sprite.Group()
    for _ in range(POP_SIZE):
        cars.add(Car( Brain() ))
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        cars_alive = [1 for car in cars if car.alive]
        if len(cars_alive) > 0:
            screen.blit(background, (0, 0))
            cars.update()
            cars.draw(background)
            screen.blit(end, endrect)
            for wall in walls:
                pygame.draw.line(screen, "black", wall[0], wall[1])
            for car in cars:
                for ray in car.rays:
                    pygame.draw.line(screen, "blue", ray[0], ray[1])
                
        else:
            best_car = max(cars, key=lambda car: car.fitness)
            best_weights = best_car.brain.get_weights()
            cars.empty()
            for i in range(POP_SIZE):
                new_brain = Brain(weights=best_weights)
                if i > 0:                    
                    new_brain.mutate(rate=0.1, scale=0.2)
                new_car = Car(brain=new_brain)
                cars.add(new_car)
            generation += 1

        pygame.display.flip()




if __name__ == '__main__': main()