import constants
import math
import random


class LineObj:
    def __init__(self):
        self.lines = []
        self.scale = 1
        self.location = (0, 0)
        self.angle = 0
        self.vector = (0, 0)

    def scaled_lines(self, k: float) -> list:
        lines_scaled = []
        for line in self.lines:
            line_scaled = []
            line_scaled[0] = (line[0][0], line[0][1] * k)
            line_scaled[1] = (line[1][0], line[1][1] * k)
            lines_scaled.append(line_scaled)
        return lines_scaled

    def location_lines(self) -> list:
        lines_cartesian = []
        for line in self.lines:
            line_cartesian = []
            line_cartesian.append((math.sin(math.radians(line[0][0])) * line[0][1] + self.location[0],
                                   math.cos(math.radians(line[0][0])) * line[0][1] + self.location[1]))
            line_cartesian.append((math.sin(math.radians(line[1][0])) * line[1][1] + self.location[0],
                                   math.cos(math.radians(line[1][0])) * line[1][1] + self.location[1]))
            lines_cartesian.append(line_cartesian)
        return lines_cartesian


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
    def __init__(self):
        super().__init__()
        self.scale = 0
        self.size = constants.ASTEROID_SCALES[self.scale]
        self.lines = self.randomized_lines()

    def randomized_lines(self,
                         segments: int = constants.ASTEROID_SEGMENTS,
                         segment_range: float = constants.ASTEROID_SEGMENT_RANGE) -> list:
        lines = []
        points = []
        for i in range(segments):
            point = (i * (360 / segments), (random.random() * 2 - 1) * segment_range + self.size)
            points.append(point)
        for index, point in enumerate(points):
            line = (point, points[index-1])
            lines.append(line)
        return lines


class Bullet:
    def __init__(self):
        self.location = (0, 0)
        self.vector = (0, 0)
