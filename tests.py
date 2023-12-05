from functions import *
from constants import *
import collision
import classes
import pygame
import random
import math


def asteroids_random_test():
    pygame.init()
    size = (700, 700)
    asteroids = []
    for i in range(ASTEROID_START_NUMBER):
        asteroid = classes.Asteroid()
        asteroid.location = on_edge()
        asteroids.append(asteroid)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    done = False
    clock = pygame.time.Clock()
    while not done:
        screen.fill((0, 0, 0))
        for asteroid in asteroids:
            asteroid.move()
            asteroid.wrap(size)
            for line in asteroid:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1])
            if random.randint(0, 200) == 1:
                asteroids += asteroid.split()
                asteroids.remove(asteroid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(FPS)


def asteroids_collide_test():
    pygame.init()
    size = (700, 700)
    asteroids = []
    for i in range(ASTEROID_START_NUMBER):
        asteroid = classes.Asteroid()
        asteroid.location = on_edge()
        asteroids.append(asteroid)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    done = False
    clock = pygame.time.Clock()
    while not done:
        screen.fill((0, 0, 0))
        for asteroid in asteroids:
            asteroid.move()
            asteroid.wrap(size)
            for line in asteroid:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1])
            for asteroid2 in asteroids:
                if asteroid != asteroid2:
                    if math.dist(asteroid.location, asteroid2.location) < \
                        (ASTEROID_SCALES[asteroid.scale] * (ASTEROID_SEGMENT_RANGE + 1) +
                         ASTEROID_SCALES[asteroid2.scale] * (ASTEROID_SEGMENT_RANGE + 1)):
                        collided = False
                        for line in asteroid:
                            for line2 in asteroid2:
                                if collision.calculate_segment_intersect(line, line2):
                                    print("collision")
                                    asteroids += asteroid.split(bullet_momentum=asteroid2.vector)
                                    asteroids += asteroid2.split(bullet_momentum=asteroid.vector)
                                    asteroids.remove(asteroid)
                                    asteroids.remove(asteroid2)
                                    collided = True
                                    break
                            if collided:
                                break
                        if collided:
                            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(FPS)


functions = [asteroids_random_test, asteroids_collide_test]
function = 1


if __name__ == "__main__":
    from sys import argv

    if "-t" in argv:
        functions[int(argv[argv.index("-t")+1])]()
    else:
        functions[function]()
