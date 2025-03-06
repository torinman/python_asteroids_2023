from constants import *
import functions
import math
import random
import collision


def set_fps(fps):
    global FPS
    FPS = fps


class LineObj:
    def __init__(self):
        self._index = 0
        self.lines = []
        self.scale = 1
        self.location = (0, 0)
        self.angle = 0
        self.vector = (0, 0)
        self.angle_vector = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.lines):
            item = self.location_line(self._index)
            self._index += 1
            return item
        else:
            self._index = 0
            raise StopIteration

    def scaled_lines(self,
                     k: float) -> list:
        lines_scaled = []
        for line in self.lines:
            line_scaled = [0, 0]
            line_scaled[0] = (line[0][0], line[0][1] * k)
            line_scaled[1] = (line[1][0], line[1][1] * k)
            lines_scaled.append(tuple(line_scaled))
        return lines_scaled

    def location_line(self,
                      index: int) -> tuple:
        line = self.lines[index]
        line_cartesian = [(math.sin(math.radians(line[0][0] + self.angle)) * line[0][1] + self.location[0],
                           math.cos(math.radians(line[0][0] + self.angle)) * line[0][1] + self.location[1]),
                          (math.sin(math.radians(line[1][0] + self.angle)) * line[1][1] + self.location[0],
                           math.cos(math.radians(line[1][0] + self.angle)) * line[1][1] + self.location[1])]
        return tuple(line_cartesian)

    def location_lines(self) -> list:
        lines_cartesian = []
        for index in range(len(self.lines)):
            line_cartesian = self.location_line(index)
            lines_cartesian.append(line_cartesian)
        return lines_cartesian

    def move(self, frames: int = 1) -> None:
        self.location = (self.location[0] + self.vector[0] * frames / FPS,
                         self.location[1] + self.vector[1] * frames / FPS)
        self.angle = self.angle + self.angle_vector * frames / FPS

    def wrap(self,
             size: tuple) -> None:
        x, y = self.location

        if self.location[0] < 0:
            x = size[0]
        elif self.location[0] > size[0]:
            x = 0

        if self.location[1] < 0:
            y = size[1]
        elif self.location[1] > size[1]:
            y = 0

        self.location = (x, y)

    def update(self,
               screen_size: tuple,
               frames: int = 1) -> None:
        self.move(frames=frames)
        self.wrap(screen_size)

    def collides_with(self,
                      item: 'LineObj') -> bool:
        for line in self:
            for line2 in item:
                if collision.calculate_segment_intersect(line, line2):
                    return True
        return False


class Ship(LineObj):
    def __init__(self):
        super().__init__()
        self.bullets = []
        self.timeout = 0

    def update(self,
               screen_size: tuple,
               frames: int = 1) -> None:
        self.move(frames=frames)
        self.wrap(screen_size)
        for bullet in self.bullets:
            bullet.location = (bullet.location[0] - bullet.vector[0] * BULLET_SIZE, bullet.location[1] - bullet.vector[1] * BULLET_SIZE)
            if bullet.location[0] > screen_size[0] or \
               bullet.location[0] < 0 or \
               bullet.location[1] > screen_size[1] or \
               bullet.location[1] < 0:
                self.bullets.remove(bullet)

    def shoot(self,
              angle: int) -> None:
        bullet = Bullet()
        bullet.location = self.location
        bullet.vector = (math.sin(math.radians(angle))*BULLET_SPEED/FPS+self.vector[0]/FPS,
                         math.cos(math.radians(angle))*BULLET_SPEED/FPS+self.vector[1]/FPS)
        self.bullets.append(bullet)


class PlayerShip(Ship):
    def __init__(self):
        super().__init__()
        self.thrusting = False
        self.lines = PLAYER_LINES
        self.lines = self.scaled_lines(PLAYER_SCALE)

    def update(self,
               screen_size: tuple,
               frames: int = 1) -> None:
        if self.thrusting:
            self.thrust(frames=frames)
        self.move(frames=frames)
        self.wrap(screen_size)
        self.vector = (self.vector[0]*PLAYER_FRICTION, self.vector[1]*PLAYER_FRICTION)
        for bullet in self.bullets:
            bullet.location = (bullet.location[0] + bullet.vector[0], bullet.location[1] + bullet.vector[1])
            if bullet.location[0] > screen_size[0] or \
               bullet.location[0] < 0 or \
               bullet.location[1] > screen_size[1] or \
               bullet.location[1] < 0:
                self.bullets.remove(bullet)

    def thrust(self,
               frames: int = 1) -> None:
        x_acceleration = math.sin(math.radians(self.angle)) * PLAYER_ACCELERATION * frames
        y_acceleration = math.cos(math.radians(self.angle)) * PLAYER_ACCELERATION * frames
        x_speed = self.vector[0] + x_acceleration
        y_speed = self.vector[1] + y_acceleration
        self.vector = (x_speed, y_speed)

    def start_thrust(self):
        self.lines = self.scaled_lines(1 / PLAYER_SCALE)
        self.lines += PLAYER_THRUST_LINES
        self.lines = self.scaled_lines(PLAYER_SCALE)
        self.thrusting = True

    def stop_thrust(self):
        self.lines = self.scaled_lines(1 / PLAYER_SCALE)
        for line in PLAYER_THRUST_LINES:
            self.lines.remove(line)
        self.lines = self.scaled_lines(PLAYER_SCALE)
        self.thrusting = False


class EnemyShip(Ship):
    def __init__(self,
                 type: int):
        super().__init__()
        self.type = type
        self.dying = False
        self.lines = ENEMY_LINES
        self.lines = self.scaled_lines(ENEMY_SCALES[self.type])
        self.vector = ((random.random()-0.5)*ENEMY_MOVEMENT_SPEED*2, (random.random()-0.5)*ENEMY_MOVEMENT_SPEED*2)
        self.accuracy = ENEMY_ACCURACIES[type]

    def update(self,
               screen_size: tuple,
               target: tuple,
               frames: int = 1) -> None:
        if not self.dying:
            self.update_movement()
            self.random_shoot(target)
            self.wrap(screen_size)
        self.move(frames=frames)
        for bullet in self.bullets:
            bullet.location = (bullet.location[0] + bullet.vector[0], bullet.location[1] + bullet.vector[1])
            if bullet.location[0] > screen_size[0] or \
               bullet.location[0] < 0 or \
               bullet.location[1] > screen_size[1] or \
               bullet.location[1] < 0:
                self.bullets.remove(bullet)

    def update_movement(self) -> None:
        if random.randint(0, FPS//ENEMY_MOVEMENT_CHANCE) == 0:
            self.vector = ((random.random()-0.5)*ENEMY_MOVEMENT_SPEED*2, (random.random()-0.5)*ENEMY_MOVEMENT_SPEED*2)

    def random_shoot(self, target):
        if random.randint(0, round(ENEMY_BULLET_FREQUENCY*FPS)) == 0:
            angle = functions.get_angle(self.location, target)
            self.shoot(angle+random.randint(round(self.accuracy)*-1, round(self.accuracy)))

    def shoot(self,
              angle: int) -> None:
        bullet = Bullet()
        bullet.location = self.location
        bullet.vector = (math.sin(math.radians(angle))*BULLET_SPEED/FPS,
                         math.cos(math.radians(angle))*BULLET_SPEED/FPS)
        self.bullets.append(bullet)


class Asteroid(LineObj):
    def __init__(self,
                 scale: int = 0,
                 location: tuple = (0, 0)):
        super().__init__()
        self.scale = scale
        self.location = location
        self.size = ASTEROID_SCALES[self.scale]
        self.lines = self.randomized_lines()
        self.angle_vector = (random.random() * 2 - 1) * (ASTEROID_SPIN_SPEED)
        speed = (random.random() * 2 - 1) * (ASTEROID_SPEED)
        angle = random.randint(0, 360)
        self.vector = (math.sin(math.radians(angle)) * speed,
                       math.cos(math.radians(angle)) * speed)

    def randomized_lines(self,
                         segments: int = ASTEROID_SEGMENTS,
                         segment_range: float = ASTEROID_SEGMENT_RANGE,
                         segment_angle_range: float = ASTEROID_SEGMENT_ANGLE_RANGE) -> list:
        lines = []
        points = []
        for i in range(segments):
            point = ((i + (random.random() * 2 - 1) * segment_angle_range) * (360 / segments),
                     (random.random() * 2 - 1) * segment_range * self.size + self.size)
            points.append(point)
        for index, point in enumerate(points):
            line = (point, points[index-1])
            lines.append(line)
        return lines

    def split(self,
              bullet_momentum: tuple = (0, 0)) -> list:
        if self.scale == len(ASTEROID_SCALES) - 1:
            return []
        momentum = ((self.vector[0] + bullet_momentum[0] * ASTEROID_BULLET_IMPACT) * ASTEROID_IMPACT,
                    (self.vector[1] + bullet_momentum[1] * ASTEROID_BULLET_IMPACT) * ASTEROID_IMPACT)
        asteroids = []
        for i in range(ASTEROID_SPLITS):
            asteroid = Asteroid(self.scale + 1, self.location)
            asteroid.vector = (asteroid.vector[0] + momentum[0],
                               asteroid.vector[1] + momentum[1])
            asteroids.append(asteroid)
        return asteroids


class Bullet:
    def __init__(self):
        self.location = (0, 0)
        self.vector = (0, 0)

    def hits(self,
             item: LineObj) -> bool:
        for line in item:
            if math.dist(line[0], self.location) < 1000:
                if collision.calculate_segment_intersect((self.location, (self.location[0] + self.vector[0],
                                                                          self.location[1] + self.vector[1])), line):
                    return True
        return False


class Explosion:
    def __init__(self) -> None:
        self._index = 0
        self.parts = []

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.parts):
            item = self.finished_line(self._index)
            self._index += 1
            return item
        else:
            self._index = 0
            raise StopIteration

    def create_parts(self,
                     location: tuple,
                     lines: list,
                     max_frames: int,
                     angle: int,
                     vector: tuple = (0, 0),
                     repetition: int = 2,
                     expansion: float = EXPLOSION_MOVEMENT_SPEED) -> None:
        for line in lines:
            for i in range(repetition):
                cartesian = self.location_line(line, angle, location)
                self.parts += [[cartesian[0], [functions.get_angle(cartesian[0], cartesian[1]),
                                               math.dist(cartesian[0], cartesian[1])],
                                random.randint(0, int(max_frames)),
                                (random.random()-0.5)*EXPLOSION_ROTATION_SPEED/FPS*2,
                                ((random.random()-0.5)*expansion*2+random.random()*vector[0], (random.random()-0.5)*expansion*2+random.random()*vector[1])]]

    def update(self) -> None:
        newparts = []
        for part in self.parts:
            if part[2] >= 0:
                part[2] -= 1
                part[1][0] += part[3]
                part[0] = (part[0][0]+part[4][0]/FPS, part[0][1]+part[4][1]/FPS)
                newparts += [part]
        self.parts = newparts

    def finished_line(self,
                      index: int) -> tuple:
        line = self.parts[index]
        line_cartesian = [line[0],
                          (math.sin(math.radians(line[1][0])) * line[1][1] + line[0][0],
                           math.cos(math.radians(line[1][0])) * line[1][1] + line[0][1])]
        return tuple(line_cartesian)

    def location_line(self,
                      line: tuple,
                      angle: int,
                      location: tuple) -> tuple:
        line_cartesian = [(math.sin(math.radians(line[0][0] + angle)) * line[0][1] + location[0],
                           math.cos(math.radians(line[0][0] + angle)) * line[0][1] + location[1]),
                          (math.sin(math.radians(line[1][0] + angle)) * line[1][1] + location[0],
                           math.cos(math.radians(line[1][0] + angle)) * line[1][1] + location[1])]
        return tuple(line_cartesian)
