import classes
import constants
import pygame


def asteroids_random_test():
    pygame.init()
    asteroid = classes.Asteroid()
    asteroid.location = (constants.ASTEROID_SCALES[0]*1.5, constants.ASTEROID_SCALES[0]*1.5)
    screen = pygame.display.set_mode((constants.ASTEROID_SCALES[0]*3, constants.ASTEROID_SCALES[0]*3))
    screen.fill((0, 0, 0))
    done = False
    clock = pygame.time.Clock()
    while not done:
        screen.fill((0, 0, 0))
        asteroid.move()
        for line in asteroid.location_lines():
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(constants.FPS)


if __name__ == "__main__":
    asteroids_random_test()
