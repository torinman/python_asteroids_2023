import constants
import math


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
            line_cartesian[0] = (math.sin(math.degrees(line[0][0])) * line[0][1] + self.location[0],
                                 math.cos(math.degrees(line[0][0])) * line[0][1] + self.location[1])
            line_cartesian[1] = (math.sin(math.degrees(line[1][0])) * line[1][1] + self.location[0],
                                 math.cos(math.degrees(line[1][0])) * line[1][1] + self.location[1])
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
        self.lines = self.randomized_lines()

    def randomized_lines(self) -> list:
        return []


class Bullet:
    def __init__(self):
        self.location = (0, 0)
        self.vector = (0, 0)
