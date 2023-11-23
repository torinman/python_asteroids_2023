import constants
import random


def on_edge(size: tuple = constants.WINDOW_SIZE) -> tuple:
    axis = random.randint(0, 1)
    distance = random.randint(0, size[axis])
    side = random.randint(0, 1)
    location = [0, 0]
    location[axis] = distance
    location[not axis] = side * size[not axis]
    return tuple(location)
