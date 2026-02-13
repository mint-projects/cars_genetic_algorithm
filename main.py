import pygame
from pygame.locals import *
from car import Car, walls, finish
from brain import Brain
import numpy as np
import random
#POLICZYĆ GDZIE PRZECINA SIĘ KAŻDY PROMIEŃ

POP_SIZE = 100
EXPECTED_WINNERS = 5

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Basic Pygame program')

    CameraX = 35
    CameraY = 75

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    clock = pygame.time.Clock()
    end = pygame.Surface([20, 100])
    end.fill("green")
    endrect = end.get_rect()
    endrect.center = finish
    generation = 1
    font = pygame.font.Font(None, 24)
    winners = []
    

    cars = pygame.sprite.Group()
    for _ in range(POP_SIZE):
        cars.add(Car( Brain() ))
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    print("ELOELOELO")
    # Event loop
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        while len(winners) < EXPECTED_WINNERS:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
            clock.tick(60)
            cars_alive = [1 for car in cars if car.alive]
            if len(cars_alive) > 0:
                cars.update()
                best_car = max(cars, key=lambda car: car.fitness)
                CameraX = best_car.x - 250
                CameraY = best_car.y - 250
                screen.fill((250, 250, 250))
                
                for wall in walls:
                    p1 = (wall[0][0] - CameraX, wall[0][1] - CameraY)
                    p2 = (wall[1][0] - CameraX, wall[1][1] - CameraY)
                    pygame.draw.line(screen, "black", p1, p2, 3)

                screen.blit(end, (finish[0] - CameraX, finish[1] - CameraY))
                for car in cars:
                    cx = car.rect.x - CameraX
                    cy = car.rect.y - CameraY
                    screen.blit(car.image, (cx, cy))
                r_start = (best_car.x - CameraX, best_car.y - CameraY)
                for ray in best_car.rays:
                    r_end = (ray[1][0] - CameraX, ray[1][1] - CameraY)
                    pygame.draw.line(screen, "blue", r_start, r_end, 1)
                if best_car.x > 498 and best_car.y > 350 and best_car.y < 450:
                    winners.append(best_car)

                info_text = font.render(f"Generation: {generation}  |  Alive: {len(cars_alive)}", True, (0, 0, 0))
                screen.blit(info_text, (10, 10))
                pygame.display.flip()  
            else:
                best_car = max(cars, key=lambda car: car.fitness)

                best_cars = sorted(cars, key=lambda car: car.fitness, reverse=True)[:10]
                best_weights = best_car.brain.get_weights()
                cars.empty()
                for k in range(POP_SIZE):
                    if k == 0:
                        if best_car.x > 498 and best_car.y > 350 and best_car.y < 450:
                            new_brain = best_car.brain.mutate(rate=0.1, scale=2)
                        else:
                            new_brain = Brain(best_weights)
                    else:
                        i, j = random.sample(range(0,10), 2)
                        new_brain = best_cars[i].brain.cross(best_cars[j].brain)             
                        new_brain.mutate(rate=0.1, scale=2)
                    new_car = Car(brain=new_brain)
                    cars.add(new_car)
                generation += 1
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            for car in winners:
                car.x, car.y = 35, 75
                car.angle = 0
                car.speed = 0
                car.alive = True
                car.frames_alive = 0
            cars.update()
            best_car = max(cars, key=lambda car: car.fitness)
            CameraX = best_car.x - 250
            CameraY = best_car.y - 250
            screen.fill((250, 250, 250))                
            for wall in walls:
                p1 = (wall[0][0] - CameraX, wall[0][1] - CameraY)
                p2 = (wall[1][0] - CameraX, wall[1][1] - CameraY)
                pygame.draw.line(screen, "black", p1, p2, 3)

            screen.blit(end, (finish[0] - CameraX, finish[1] - CameraY))
            for car in cars:
                cx = car.rect.x - CameraX
                cy = car.rect.y - CameraY
                screen.blit(car.image, (cx, cy))

            info_text = font.render(f"All {EXPECTED_WINNERS} winners", True, (0, 0, 0))
            screen.blit(info_text, (10, 10))
            pygame.display.flip()  
            
            
                    
            
        



if __name__ == '__main__': main()