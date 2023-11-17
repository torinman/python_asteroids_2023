import classes
import constants
import pygame
import random


def asteroids_random_test():
    pygame.init()
    asteroids = [classes.Asteroid(), classes.Asteroid()]
    for asteroid in asteroids:
        asteroid.location = (350, 350)
    screen = pygame.display.set_mode((700, 700))
    screen.fill((0, 0, 0))
    done = False
    clock = pygame.time.Clock()
    while not done:
        screen.fill((0, 0, 0))
        for asteroid in asteroids:
            asteroid.move()
            for line in asteroid.location_lines():
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1])
            if random.randint(0, 200) == 1:
                asteroids += asteroid.split()
                asteroids.remove(asteroid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(constants.FPS)


if __name__ == "__main__":
    asteroids_random_test()
