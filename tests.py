from functions import *
from constants import *
import classes
import pygame
import random
import math


def asteroids_random_test():
    pygame.init()
    size = WINDOW_SIZE
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
    size = WINDOW_SIZE
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
    size = WINDOW_SIZE
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
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        for bullet in player.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS/60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS/60) * BULLET_SIZE), width=LINE_THICKNESS)
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
    size = WINDOW_SIZE
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    current_asteroids = ASTEROID_START_NUMBER
    asteroids = create_asteroids(size, current_asteroids)
    done = False
    clock = pygame.time.Clock()
    player = classes.PlayerShip()
    player.location = (size[0] / 2, size[1] / 2)
    while not done:
        screen.fill((0, 0, 0))
        player.update(size)
        for line in player:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        for bullet in player.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS/60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS/60) * BULLET_SIZE), width=LINE_THICKNESS)
        for asteroid in asteroids:
            asteroid.update(size)
            for line in asteroid:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
            for bullet in player.bullets:
                if bullet.hits(asteroid):
                    asteroids += asteroid.split(bullet.vector)
                    asteroids.remove(asteroid)
                    player.bullets.remove(bullet)
                    if not asteroids:
                        current_asteroids += 2
                        asteroids = create_asteroids(size, current_asteroids)
                    break
            if asteroid.collides_with(player):
                done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.WINDOWRESIZED:
                previous_size = size
                size = pygame.display.get_window_size()
                player.location = (player.location[0]*size[0]/previous_size[0], player.location[1]*size[1]/previous_size[1])
                for asteroid in asteroids:
                    asteroid.location = (asteroid.location[0] * size[0] / previous_size[0], asteroid.location[1] * size[1] / previous_size[1])
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


def enemy_movement_test():
    pygame.init()
    size = WINDOW_SIZE
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    done = False
    clock = pygame.time.Clock()
    enemy = classes.EnemyShip(0)
    enemy.location = (size[0] / 2, size[1] / 2)
    while not done:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.WINDOWRESIZED:
                size = pygame.display.get_window_size()
        enemy.update(size, (0, 0))
        for line in enemy:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        pygame.display.flip()
        clock.tick(FPS)


def big_enemy_vs_asteroids_test():
    pygame.init()
    size = WINDOW_SIZE
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    done = False
    current_asteroids = ASTEROID_START_NUMBER
    asteroids = create_asteroids(size, current_asteroids)
    clock = pygame.time.Clock()
    enemy = classes.EnemyShip(1)
    enemy.location = (size[0] / 2, size[1] / 2)
    while not done:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.WINDOWRESIZED:
                size = pygame.display.get_window_size()
        for bullet in enemy.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS / 60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS / 60) * BULLET_SIZE), width=LINE_THICKNESS)
        for asteroid in asteroids:
            asteroid.update(size)
            for line in asteroid:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
            for bullet in enemy.bullets:
                if bullet.hits(asteroid):
                    asteroids += asteroid.split(bullet.vector)
                    asteroids.remove(asteroid)
                    enemy.bullets.remove(bullet)
                    if not asteroids:
                        current_asteroids += 2
                        asteroids = create_asteroids(size, current_asteroids)
            if asteroid.collides_with(enemy):
                asteroids += asteroid.split(enemy.vector)
                asteroids.remove(asteroid)
                newenemy = classes.EnemyShip(1)
                newenemy.location = (size[0] / 2, size[1] / 2)
                newenemy.bullets = enemy.bullets
                enemy = newenemy
                if not asteroids:
                    current_asteroids += 2
                    asteroids = create_asteroids(size, current_asteroids) 
        enemy.update(size, (0, 0))
        for line in enemy:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        pygame.display.flip()
        clock.tick(FPS)


def small_enemy_target_test():
    pygame.init()
    size = WINDOW_SIZE
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    done = False
    target = (size[0] / 2, size[1] / 2)
    clock = pygame.time.Clock()
    enemy = classes.EnemyShip(0)
    while not done:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.WINDOWRESIZED:
                size = pygame.display.get_window_size()
                target = (size[0] / 2, size[1] / 2)
        enemy.update(size, target)
        for bullet in enemy.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS / 60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS / 60) * BULLET_SIZE), width=LINE_THICKNESS)
        for line in enemy:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        pygame.draw.circle(screen, (255, 255, 255), target, 10)
        pygame.display.flip()
        clock.tick(FPS)


def asteroids_explosion_test():
    pygame.init()
    size = WINDOW_SIZE
    asteroids = []
    for i in range(ASTEROID_START_NUMBER):
        asteroid = classes.Asteroid()
        asteroid.location = on_edge()
        asteroids.append(asteroid)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    done = False
    clock = pygame.time.Clock()
    explosion = classes.Explosion()
    while not done:
        screen.fill((0, 0, 0))
        for asteroid in asteroids:
            asteroid.update(size)
            for line in asteroid:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
            if random.randint(0, 200) == 1:
                asteroids += asteroid.split()
                explosion.create_parts(asteroid.location, asteroid.lines, FPS, asteroid.angle, vector=asteroid.vector, repetition=1, expansion=ASTEROID_SCALES[asteroid.scale]/FPS*2)
                asteroids.remove(asteroid)
        for line in explosion:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        explosion.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(FPS)


def ship_test_asteroids_explosion():
    pygame.init()
    size = WINDOW_SIZE
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    current_asteroids = ASTEROID_START_NUMBER
    asteroids = create_asteroids(size, current_asteroids)
    done = False
    clock = pygame.time.Clock()
    player = classes.PlayerShip()
    player.location = (size[0] / 2, size[1] / 2)
    explosion = classes.Explosion()
    while not done:
        screen.fill((0, 0, 0))
        player.update(size)
        for line in player:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        explosion.update()
        for line in explosion:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        for bullet in player.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS/60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS/60) *  BULLET_SIZE), width=LINE_THICKNESS)
        for asteroid in asteroids:
            asteroid.update(size)
            for line in asteroid:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
            for bullet in player.bullets:
                if bullet.hits(asteroid):
                    asteroids += asteroid.split(bullet.vector)
                    explosion.create_parts(asteroid.location, asteroid.lines, FPS*0.7, asteroid.angle,
                                           vector=asteroid.vector, repetition=1,
                                           expansion=ASTEROID_SCALES[asteroid.scale] / FPS * 3)
                    asteroids.remove(asteroid)
                    player.bullets.remove(bullet)
                    if not asteroids:
                        current_asteroids += 2
                        asteroids = create_asteroids(size, current_asteroids)
                    break
            if asteroid.collides_with(player):
                done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.WINDOWRESIZED:
                previous_size = size
                size = pygame.display.get_window_size()
                player.location = (player.location[0]*size[0]/previous_size[0], player.location[1]*size[1]/previous_size[1])
                for asteroid in asteroids:
                    asteroid.location = (asteroid.location[0] * size[0] / previous_size[0], asteroid.location[1] * size[1] / previous_size[1])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.start_thrust()
                elif event.key == pygame.K_LEFT:
                    player.angle_vector += PLAYER_ANGLE_SPEED
                elif event.key == pygame.K_RIGHT:
                    player.angle_vector -= PLAYER_ANGLE_SPEED
                elif event.key == pygame.K_SPACE:
                    player.shoot(player.angle)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.stop_thrust()
                elif event.key == pygame.K_LEFT:
                    player.angle_vector -= PLAYER_ANGLE_SPEED
                elif event.key == pygame.K_RIGHT:
                    player.angle_vector += PLAYER_ANGLE_SPEED
        pygame.display.flip()
        clock.tick(FPS)


def delta_time_test():
    global FPS
    keys_down = []
    pygame.init()
    size = WINDOW_SIZE
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    current_asteroids = ASTEROID_START_NUMBER
    asteroids = create_asteroids(size, current_asteroids)
    done = False
    clock = pygame.time.Clock()
    player = classes.PlayerShip()
    player.location = (size[0] / 2, size[1] / 2)
    explosion = classes.Explosion()
    while not done:
        screen.fill((0, 0, 0))
        player.update(size)
        for line in player:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        explosion.update()
        for line in explosion:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        for bullet in player.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS/60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS/60) * BULLET_SIZE), width=LINE_THICKNESS)
        for asteroid in asteroids:
            asteroid.update(size)
            for line in asteroid:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
            for bullet in player.bullets:
                if bullet.hits(asteroid):
                    asteroids += asteroid.split(bullet.vector)
                    explosion.create_parts(asteroid.location, asteroid.lines, FPS, asteroid.angle,
                                           vector=asteroid.vector, repetition=1,
                                           expansion=ASTEROID_SCALES[asteroid.scale] / FPS * 2)
                    asteroids.remove(asteroid)
                    player.bullets.remove(bullet)
                    if not asteroids:
                        current_asteroids += ASTEROID_NUMBER_INCREASE
                        asteroids = create_asteroids(size, current_asteroids)
                    break
            if asteroid.collides_with(player):
                done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.WINDOWRESIZED:
                previous_size = size
                size = pygame.display.get_window_size()
                player.location = (player.location[0]*size[0]/previous_size[0], player.location[1]*size[1]/previous_size[1])
                for asteroid in asteroids:
                    asteroid.location = (asteroid.location[0] * size[0] / previous_size[0], asteroid.location[1] * size[1] / previous_size[1])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                       player.shoot(player.angle)
                if event.key == pygame.K_UP:
                    player.start_thrust()
                else:
                    keys_down.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.stop_thrust()
                else:
                    keys_down.remove(event.key)
        if pygame.K_LEFT in keys_down:
            player.angle += PLAYER_ANGLE_SPEED / FPS
        if pygame.K_RIGHT in keys_down:
            player.angle -= PLAYER_ANGLE_SPEED / FPS
        pygame.display.flip()
        clock.tick(FPS)
        delta = clock.get_fps()
        if delta:
            FPS = delta
            classes.set_fps(delta)


def ship_test_enemy():
    pygame.init()
    size = WINDOW_SIZE
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    done = False
    clock = pygame.time.Clock()
    player = classes.PlayerShip()
    player.location = (size[0] / 2, size[1] / 2)
    enemy_accuracy = ENEMY_ACCURACIES[0]
    enemy = classes.EnemyShip(random.randint(0, 1))
    explosion = classes.Explosion()
    keys_down = []
    while not done:
        screen.fill((0, 0, 0))
        player.update(size)
        if enemy.dying and not pygame.Rect((0, 0, size[0], size[1])).collidepoint(enemy.location):
            type = random.randint(0, 1)
            bullets = enemy.bullets
            enemy = classes.EnemyShip(type)
            enemy.bullets = bullets
            enemy_accuracy *= SMALL_BULLET_ACCURACY_INCREASE
            if enemy.type == 0:
                enemy.accuracy = enemy_accuracy
        if player.timeout:
            player.timeout -= 1
        else:
            for line in player:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        for bullet in player.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS/60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS/60) * BULLET_SIZE), width=LINE_THICKNESS)
            if bullet.hits(enemy):
                player.bullets.remove(bullet)
                type = random.randint(0, 1)
                explosion.create_parts(enemy.location, enemy.lines, FPS*EXPLOSION_DECAY_SECONDS, 0, enemy.vector)
                bullets = enemy.bullets
                enemy = classes.EnemyShip(type)
                enemy.bullets = bullets
                enemy_accuracy *= SMALL_BULLET_ACCURACY_INCREASE
                if enemy.type == 0:
                    enemy.accuracy = enemy_accuracy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.WINDOWRESIZED:
                size = pygame.display.get_window_size()
            elif event.type == pygame.KEYDOWN:
                keys_down.append(event.key)
                if event.key == pygame.K_SPACE and not player.timeout:
                    player.shoot(player.angle)
                if event.key == pygame.K_UP:
                    player.start_thrust()
                    player.thrusting = False
            elif event.type == pygame.KEYUP:
                keys_down.remove(event.key)
                if event.key == pygame.K_UP:
                    player.stop_thrust()
        if not player.timeout:
            if pygame.K_LEFT in keys_down:
                player.angle += PLAYER_ANGLE_SPEED / FPS
            if pygame.K_RIGHT in keys_down:
                player.angle -= PLAYER_ANGLE_SPEED / FPS
            if pygame.K_UP in keys_down:
                player.thrust()
        explosion.update()
        for line in explosion:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        enemy.update(size, player.location)
        for line in enemy:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        for bullet in enemy.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS / 60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS / 60) * BULLET_SIZE), width=LINE_THICKNESS)
            if bullet.hits(player) and not player.timeout:
                enemy.bullets.remove(bullet)
                explosion.create_parts(player.location, player.lines, FPS * EXPLOSION_DECAY_SECONDS, player.angle, player.vector)
                player.location = (size[0]/2, size[1]/2)
                player.vector = (0, 0)
                player.timeout = PLAYER_OUT*FPS
                enemy.dying = True
        if player.collides_with(enemy):
            explosion.create_parts(player.location, player.lines, FPS * EXPLOSION_DECAY_SECONDS, player.angle, player.vector)
            player.location = (size[0]/2, size[1]/2)
            player.vector = (0, 0)
            player.timeout = PLAYER_OUT*FPS
            type = random.randint(0, 1)
            explosion.create_parts(enemy.location, enemy.lines, FPS * EXPLOSION_DECAY_SECONDS, 0, enemy.vector)
            bullets = enemy.bullets
            enemy = classes.EnemyShip(type)
            enemy.bullets = bullets
            enemy_accuracy *= SMALL_BULLET_ACCURACY_INCREASE
            if enemy.type == 0:
                enemy.accuracy = enemy_accuracy
        pygame.display.flip()
        clock.tick(FPS)


functions = [asteroids_random_test,          # 0
             asteroids_collide_test,         # 1
             ship_test,                      # 2
             ship_test_asteroids,            # 3
             enemy_movement_test,            # 4
             big_enemy_vs_asteroids_test,    # 5
             small_enemy_target_test,        # 6
             asteroids_explosion_test,       # 7
             ship_test_asteroids_explosion,  # 8
             delta_time_test,                # 9
             ship_test_enemy]                # 10
function = 10


if __name__ == "__main__":
    from sys import argv

    if "-t" in argv:
        functions[int(argv[argv.index("-t")+1])]()
    else:
        functions[function]()
