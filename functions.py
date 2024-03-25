import constants
import random
import classes


def on_edge(size: tuple = constants.WINDOW_SIZE) -> tuple:
    axis = random.randint(0, 1)
    distance = random.randint(0, size[axis])
    side = random.randint(0, 1)
    location = [0, 0]
    location[axis] = distance
    location[not axis] = side * size[not axis]
    return tuple(location)


def create_asteroids(number: int = constants.ASTEROID_START_NUMBER) -> list:
    asteroids = []
    for i in range(number):
        asteroid = classes.Asteroid()
        asteroid.location = on_edge()
        asteroids.append(asteroid)
    return asteroids
