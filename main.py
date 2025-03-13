#   asteroids_main.py
#
#   A rewriting of my 2020-2021 python recreation of the arcade game Asteroids,
#   using better code practices and the experience I have gained over the past
#   2 and a half years since I made the original.
#
# 	I've never actually played the original game,
# 	so I have based this on YouTube videos and talking to people who have played it
#
# 	Game keys used are either Q for thrust, A for shoot and OP for rotation;
# 	or Up for Thrust, Space for shoot and Left and Right for Rotate.
# 	H for hyperspace jump.
#
# 	The program requires PyGame and Python 3
#
# 	Sound files all created by Torin Stephens
#
# 	Tested and developed under PyGame 2.1.2 and Python 3.8.5
#
#  	This program is free software: you can redistribute it and/or modify
#  	it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see  <https://www.gnu.org/licenses/>.
import random

import pygame
from constants import *
from functions import *

def main():
    global FPS
    lives = PLAYER_LIVES
    keys_down = []
    pygame.init()
    size = WINDOW_SIZE
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    pygame.display.set_caption("Asteroids by Torin")
    screen.fill((0, 0, 0))
    current_asteroids = ASTEROID_START_NUMBER
    asteroids = create_asteroids(size, current_asteroids)
    done = False
    clock = pygame.time.Clock()
    player = classes.PlayerShip()
    player.location = (size[0] / 2, size[1] / 2)
    explosion = classes.Explosion()
    enemies = []
    enemy_accuracy = ENEMY_ACCURACIES[0]
    while not done:
        screen.fill((0, 0, 0))
        for i in range(ENEMY_AMOUNT-len(enemies)):
            if random.randint(0, round(ENEMY_TIME*FPS)) == 0:
                type = random.randint(0, 1)
                enemy = classes.EnemyShip(type)
                enemy_accuracy *= SMALL_BULLET_ACCURACY_INCREASE
                if enemy.type == 0:
                    enemy.accuracy = enemy_accuracy
                enemies.append(enemy)
        player.update(size)
        for enemy in enemies:
            enemy.update(size, player.location, shoot=not player.timeout)
            for line in enemy:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
            for bullet in enemy.bullets:
                pygame.draw.line(screen, (255, 255, 255), bullet.location,
                                 (bullet.location[0] - bullet.vector[0] * (FPS / 60) * BULLET_SIZE,
                                  bullet.location[1] - bullet.vector[1] * (FPS / 60) * BULLET_SIZE),
                                 width=LINE_THICKNESS)
                if bullet.hits(player) and not player.timeout:
                    enemy.bullets.remove(bullet)
                    explosion.create_parts(player.location, player.lines, FPS * EXPLOSION_DECAY_SECONDS, player.angle,
                                           player.vector)
                    player.location = (size[0] / 2, size[1] / 2)
                    player.vector = (0, 0)
                    enemy.dying = True
                    player.timeout = round(PLAYER_OUT * FPS)
            if not player.timeout:
                if player.collides_with(enemy):
                    explosion.create_parts(player.location, player.lines, FPS * EXPLOSION_DECAY_SECONDS, player.angle,
                                           player.vector)
                    player.location = (size[0] / 2, size[1] / 2)
                    player.vector = (0, 0)
                    player.timeout = round(PLAYER_OUT * FPS)
                    enemies.remove(enemy)
                    explosion.create_parts(enemy.location, enemy.lines, FPS * EXPLOSION_DECAY_SECONDS, 0, enemy.vector)
            if enemy.dying and not pygame.Rect((0, 0, size[0], size[1])).collidepoint(enemy.location):
                enemies.remove(enemy)
        if player.timeout > 0:
            player.timeout -= 1
        else:
            for line in player:
                pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        explosion.update()
        for line in explosion:
            pygame.draw.line(screen, (255, 255, 255), line[0], line[1], width=LINE_THICKNESS)
        for bullet in player.bullets:
            pygame.draw.line(screen, (255, 255, 255), bullet.location,
                             (bullet.location[0] - bullet.vector[0] * (FPS/60) * BULLET_SIZE,
                              bullet.location[1] - bullet.vector[1] * (FPS/60) * BULLET_SIZE), width=LINE_THICKNESS)
            for enemy in enemies:
                if bullet.hits(enemy):
                    player.bullets.remove(bullet)
                    explosion.create_parts(enemy.location, enemy.lines, FPS * EXPLOSION_DECAY_SECONDS, 0, enemy.vector)
                    enemies.remove(enemy)
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
            if not player.timeout:
                if asteroid.collides_with(player):
                    explosion.create_parts(player.location, player.lines*EXPLOSION_PLAYER_MULTIPLIER, FPS * EXPLOSION_DECAY_SECONDS, player.angle,
                                           player.vector)
                    lives -= 1
                    if not lives:
                        done = True
                    player.timeout = round(PLAYER_OUT * FPS)
                    player.location = (size[0] / 2, size[1] / 2)
                    player.vector = (0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.WINDOWRESIZED:
                previous_size = size
                size = pygame.display.get_window_size()
                player.location = (
                player.location[0] * size[0] / previous_size[0], player.location[1] * size[1] / previous_size[1])
                for asteroid in asteroids:
                    asteroid.location = (asteroid.location[0] * size[0] / previous_size[0],
                                         asteroid.location[1] * size[1] / previous_size[1])
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
        pygame.display.flip()
        clock.tick(FPS)
        delta = clock.get_fps()
        if delta:
            FPS = delta
            classes.set_fps(delta)


if __name__ == "__main__":
    main()
