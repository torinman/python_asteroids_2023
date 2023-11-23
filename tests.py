from functions import *
from constants import *
import classes
import pygame
import random


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
            for line in asteroid.location_lines():
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1])
            if random.randint(0, 200) == 1:
                asteroids += asteroid.split()
                asteroids.remove(asteroid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(FPS)


functions = [asteroids_random_test]
function = 0


if __name__ == "__main__":
    from sys import argv

    if "-t" in argv:
        functions[int(argv[argv.index("-t")+1])]()
    else:
        functions[function]()
