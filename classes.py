import constants


class LineObj:
    def __init__(self):
        self.lines = []
        self.scale = 1
        self.location = (0, 0)
        self.angle = 0
        self.x_momentum = 0
        self.y_momentum = 0

    def scaled_lines(self, k) -> list:
        lines_scaled = []
        for line in self.lines:
            lines_scaled.append(((line[0][0], line[0][1]*k), (line[1][0], line[1][1]*k)))
        return lines_scaled

    def location_lines(self) -> list:
        pass


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
