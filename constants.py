# game constants
FPS = 30
WINDOW_SIZE = (700, 700)
LINE_THICKNESS = 1

# class constants

# asteroid constants
ASTEROID_SCALES = [40, 20, 10]
ASTEROID_SCORES = [20, 50, 100]
ASTEROID_START_NUMBER = 4
ASTEROID_NUMBER_INCREASE = 2
ASTEROID_SEGMENTS = 20
ASTEROID_SEGMENT_ANGLE_RANGE = 0.7
ASTEROID_SEGMENT_RANGE = 0.3
ASTEROID_SPIN_SPEED = 120
ASTEROID_SPEED = 100
ASTEROID_BULLET_IMPACT = 0.2
ASTEROID_IMPACT = 0.5
ASTEROID_SPLITS = 2

# ship constants
BULLET_SPEED = 420
BULLET_SIZE = 3

# player ship constants
PLAYER_LINES = [((0, 1), (150, 1)), ((0, 1), (210, 1)), ((0, 0), (150, 1)), ((0, 0), (210, 1))]
PLAYER_THRUST_LINES = [((150, 0.5), (180, 1)), ((210, 0.5), (180, 1))]
PLAYER_SCALE = 20
PLAYER_ACCELERATION = 6
PLAYER_FRICTION = 0.995
PLAYER_ANGLE_SPEED = 200
PLAYER_OUT = 3

# enemy ship constants
ENEMY_LINES = [((90, 1), (270, 1)), ((90, 1), (125, 0.65)), ((90, 1), (55, 0.65)), ((270, 1), (305, 0.65)), ((270, 1), (235, 0.65)), ((55, 0.65), (305, 0.65)), ((235, 0.65), (125, 0.65)), ((125, 0.65), (150, 0.9)), ((235, 0.65), (210, 0.9)), ((150, 0.9), (210, 0.9))]
ENEMY_MOVEMENT_SPEED = 120
ENEMY_MOVEMENT_CHANCE = 0.8
ENEMY_SCALES = [15, 25]
ENEMY_BULLET_FREQUENCY = 0.8
ENEMY_ACCURACIES = (50, 180)
SMALL_BULLET_ACCURACY_INCREASE = 0.9

# explosion constants
EXPLOSION_MOVEMENT_SPEED = 100
EXPLOSION_ROTATION_SPEED = 180
EXPLOSION_DECAY_SECONDS = 2
