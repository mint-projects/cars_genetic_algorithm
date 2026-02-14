import pygame
from pygame.locals import *
from car import Car, walls, finish, START_POS
from brain import Brain
import random

POP_SIZE = 200
EXPECTED_WINNERS = 5
GRASS_COLOR = (34, 139, 34)
ROAD_COLOR = (105, 105, 105)
WALL_COLOR = (0, 0, 0)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


track_polygon_points = [
    (0, 50),
    (250, 50),
    (250, 350),
    (500, 350),
    (500, 450),
    (150, 450),
    (150, 150),
    (0, 150),
]


def main():

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("backingtrack.wav")
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Cars")

    CameraX = START_POS[0]
    CameraY = START_POS[1]

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GRASS_COLOR)

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
        cars.add(Car(Brain()))

    screen.blit(background, (0, 0))
    pygame.draw.polygon(screen, ROAD_COLOR, track_polygon_points, 0)
    pygame.display.flip()

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
            cars_alive = [car for car in cars if car.alive]
            if len(cars_alive) > 0:
                cars.update()
                best_car = max(cars_alive, key=lambda car: car.fitness)
                CameraX = best_car.x - SCREEN_WIDTH // 2
                CameraY = best_car.y - SCREEN_HEIGHT // 2
                screen.fill(GRASS_COLOR)
                shifted_track_poly = []
                for point in track_polygon_points:
                    shifted_x = point[0] - CameraX
                    shifted_y = point[1] - CameraY
                    shifted_track_poly.append((shifted_x, shifted_y))
                pygame.draw.polygon(screen, ROAD_COLOR, shifted_track_poly, 0)

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
                for car in cars_alive:
                    if car.x > 498 and car.y > 350 and car.y < 450:
                        winners.append(car.brain)
                        car.alive = False

                info_text = font.render(
                    f"Generation: {generation}  |  Alive: {len(cars_alive)}",
                    True,
                    (0, 0, 0),
                )
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
                            weights = best_car.brain.get_weights()
                            new_brain = Brain(weights)
                            new_brain.mutate(rate=0.1, scale=8)
                        else:
                            new_brain = Brain(best_weights)
                    else:
                        i, j = random.sample(range(0, 10), 2)
                        new_brain = best_cars[i].brain.cross(best_cars[j].brain)
                        new_brain.mutate(rate=0.1, scale=10)
                    new_car = Car(brain=new_brain)
                    cars.add(new_car)
                generation += 1
        screen.blit(background, (0, 0))
        pygame.display.flip()
        winners_group = pygame.sprite.Group()

        for brain in winners:
            car = Car(brain)
            car.x, car.y = 45, 100
            car.angle = 0
            car.speed = 0
            car.alive = True
            car.frames_alive = 0
            car.fitness = 0
            car.passed_checkpoints = []
            winners_group.add(car)

        while True:
            all_finished = True
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            winners_group.update()
            for car in winners_group:
                if (car.x > 498 and 350 < car.y < 450):
                    car.alive = False
                if car.alive:
                    all_finished = False

            leader = max(winners_group, key=lambda car: car.fitness)
            CameraX = leader.x - SCREEN_WIDTH // 2
            CameraY = leader.y - SCREEN_HEIGHT // 2

            screen.fill(GRASS_COLOR)
            shifted_track_poly = []
            for point in track_polygon_points:
                shifted_x = point[0] - CameraX
                shifted_y = point[1] - CameraY
                shifted_track_poly.append((shifted_x, shifted_y))

            pygame.draw.polygon(screen, ROAD_COLOR, shifted_track_poly, 0)

            for wall in walls:
                p1 = (wall[0][0] - CameraX, wall[0][1] - CameraY)
                p2 = (wall[1][0] - CameraX, wall[1][1] - CameraY)
                pygame.draw.line(screen, "black", p1, p2, 3)

            screen.blit(end, (finish[0] - CameraX, finish[1] - CameraY))

            for car in winners_group:
                cx = car.rect.x - CameraX
                cy = car.rect.y - CameraY
                screen.blit(car.image, (cx, cy))
                
            if all_finished == True:
                for car in winners_group:
                    if not car.alive or (car.x > 498 and 350 < car.y < 450):
                        car.x, car.y = 45, 100
                        car.angle = 0
                        car.speed = 0
                        car.alive = True
                        car.frames_alive = 0

            info_text = font.render(f"Winners!!!", True, (61, 34, 186))
            screen.blit(info_text, (10, 10))

            pygame.display.flip()


if __name__ == "__main__":
    main()
