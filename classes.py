from constants import *
import math
import random


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
            raise StopIteration

    def scaled_lines(self,
                     k: float) -> list:
        lines_scaled = []
        for line in self.lines:
            line_scaled = []
            line_scaled[0] = (line[0][0], line[0][1] * k)
            line_scaled[1] = (line[1][0], line[1][1] * k)
            lines_scaled.append(line_scaled)
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
        self.location = (self.location[0] + self.vector[0] * frames,
                         self.location[1] + self.vector[1] * frames)
        self.angle = self.angle + self.angle_vector * frames

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


class Ship(LineObj):
    def __init__(self):
        super().__init__()
        self.bullets = []


class PlayerShip(Ship):
    def __init__(self):
        super().__init__()


class EnemyShip(Ship):
    def __init__(self):
        super().__init__()


class Asteroid(LineObj):
    def __init__(self,
                 scale: int = 0,
                 location: tuple = (0, 0)):
        super().__init__()
        self.scale = scale
        self.location = location
        self.size = ASTEROID_SCALES[self.scale]
        self.lines = self.randomized_lines()
        self.angle_vector = (random.random() * 2 - 1) * (ASTEROID_SPIN_SPEED / FPS)
        speed = (random.random() * 2 - 1) * (ASTEROID_SPEED / FPS)
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
    def __init__(self, ):
        self.location = (0, 0)
        self.vector = (0, 0)
