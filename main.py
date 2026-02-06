import pygame
from pygame.locals import *
from car import Car, walls
from brain import Brain
import numpy as np
#POLICZYĆ GDZIE PRZECINA SIĘ KAŻDY PROMIEŃ

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    temp_car = Car()
    pygame.display.set_caption('Basic Pygame program')

    nn = Brain()

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
    

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        temp_car.update()
        temp_car.calculate_intersection_point(walls)
        where = np.argmax(nn.predict(temp_car.distances))
        if where == 0:
            temp_car.x += 1
        elif where == 1:
            temp_car.y += 1
        elif where == 2:
            temp_car.x -= 1
        else:
            temp_car.y += 1

        screen.blit(background, (0, 0))
        screen.blit(temp_car.image, temp_car.rect)
        for wall in walls:
            pygame.draw.line(screen, "black", wall[0], wall[1])
        for ray in temp_car.rays:
            pygame.draw.line(screen, "blue", ray[0], ray[1])
        pygame.display.flip()


if __name__ == '__main__': main()