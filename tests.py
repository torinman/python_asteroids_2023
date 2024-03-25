from functions import *
from constants import *
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
            asteroid.update(size)
            for line in asteroid:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
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
            asteroid.update(size)
            for line in asteroid:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
            for asteroid2 in asteroids:
                if asteroid != asteroid2:
                    if math.dist(asteroid.location, asteroid2.location) < \
                        (ASTEROID_SCALES[asteroid.scale] * (ASTEROID_SEGMENT_RANGE + 1) +
                         ASTEROID_SCALES[asteroid2.scale] * (ASTEROID_SEGMENT_RANGE + 1)):
                        if asteroid.collides_with(asteroid2):
                            print("collision")
                            asteroids += asteroid.split(bullet_momentum=asteroid2.vector)
                            asteroids += asteroid2.split(bullet_momentum=asteroid.vector)
                            asteroids.remove(asteroid)
                            asteroids.remove(asteroid2)
                            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(FPS)


def ship_test():
    pygame.init()
    size = (700, 700)
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    done = False
    clock = pygame.time.Clock()
    player = classes.PlayerShip()
    player.location = (size[0] / 2, size[1] / 2)
    while not done:
        screen.fill((0, 0, 0))
        player.update(size)
        for line in player:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1])
        for bullet in player.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS/60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS/60) * BULLET_SIZE))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.WINDOWRESIZED:
                size = pygame.display.get_window_size()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.start_thrust()
                elif event.key == pygame.K_LEFT:
                    player.angle_vector += PLAYER_ANGLE_SPEED/FPS
                elif event.key == pygame.K_RIGHT:
                    player.angle_vector -= PLAYER_ANGLE_SPEED/FPS
                elif event.key == pygame.K_SPACE:
                    player.shoot(player.angle)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.stop_thrust()
                elif event.key == pygame.K_LEFT:
                    player.angle_vector -= PLAYER_ANGLE_SPEED/FPS
                elif event.key == pygame.K_RIGHT:
                    player.angle_vector += PLAYER_ANGLE_SPEED/FPS
        pygame.display.flip()
        clock.tick(FPS)


def ship_test_asteroids():
    pygame.init()
    size = (700, 700)
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    current_asteroids = ASTEROID_START_NUMBER
    asteroids = create_asteroids(current_asteroids)
    done = False
    clock = pygame.time.Clock()
    player = classes.PlayerShip()
    player.location = (size[0] / 2, size[1] / 2)
    while not done:
        screen.fill((0, 0, 0))
        player.update(size)
        for line in player:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1])
        for bullet in player.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS/60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS/60) * BULLET_SIZE))
        for asteroid in asteroids:
            asteroid.update(size)
            for line in asteroid:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
            for bullet in player.bullets:
                if bullet.hits(asteroid):
                    asteroids += asteroid.split(bullet.vector)
                    asteroids.remove(asteroid)
                    player.bullets.remove(bullet)
                    if asteroids == []:
                        current_asteroids += 2
                        asteroids = create_asteroids(current_asteroids)
            if asteroid.collides_with(player):
               done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.WINDOWRESIZED:
                size = pygame.display.get_window_size()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.start_thrust()
                elif event.key == pygame.K_LEFT:
                    player.angle_vector += PLAYER_ANGLE_SPEED/FPS
                elif event.key == pygame.K_RIGHT:
                    player.angle_vector -= PLAYER_ANGLE_SPEED/FPS
                elif event.key == pygame.K_SPACE:
                    player.shoot(player.angle)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.stop_thrust()
                elif event.key == pygame.K_LEFT:
                    player.angle_vector -= PLAYER_ANGLE_SPEED/FPS
                elif event.key == pygame.K_RIGHT:
                    player.angle_vector += PLAYER_ANGLE_SPEED/FPS
        pygame.display.flip()
        clock.tick(FPS)


functions = [asteroids_random_test, asteroids_collide_test, ship_test, ship_test_asteroids]
function = 3


if __name__ == "__main__":
    from sys import argv

    if "-t" in argv:
        functions[int(argv[argv.index("-t")+1])]()
    else:
        functions[function]()
