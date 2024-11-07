import constants
import random
import classes
import math


def on_edge(size: tuple = constants.WINDOW_SIZE) -> tuple:
    axis = random.randint(0, 1)
    distance = random.randint(0, size[axis])
    side = random.randint(0, 1)
    location = [0, 0]
    location[axis] = distance
    location[not axis] = side * size[not axis]
    return tuple(location)


def create_asteroids(size: tuple,
                     number: int = constants.ASTEROID_START_NUMBER) -> list:
    asteroids = []
    for i in range(number):
        asteroid = classes.Asteroid()
        asteroid.location = on_edge(size)
        asteroids.append(asteroid)
    return asteroids


def get_angle(p1, p2):
    dist = math.dist(p1, p2)
    sin = (p2[0]-p1[0])/dist
    angle = math.degrees(math.asin(sin))
    if p1[1] > p2[1]:
        angle = (angle-180)*-1
    return angle
