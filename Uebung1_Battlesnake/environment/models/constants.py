from enum import Enum


class Direction(Enum):
    UP = 'up'
    RIGHT = 'right'
    DOWN = 'down'
    LEFT = 'left'


class DirectionUtil:

    @staticmethod
    def is_same(a: Direction, b: Direction):
        return a == b

    @staticmethod
    def is_flipped(a: Direction, b: Direction):
        return (a == Direction.UP and b == Direction.DOWN) or \
            (a == Direction.RIGHT and b == Direction.LEFT) or \
            (a == Direction.DOWN and b == Direction.UP) or \
            (a == Direction.LEFT and b == Direction.RIGHT)

    @staticmethod
    def is_rotated_clockwise(a: Direction, b: Direction):
        return (a == Direction.UP and b == Direction.RIGHT) or \
               (a == Direction.RIGHT and b == Direction.DOWN) or \
               (a == Direction.DOWN and b == Direction.LEFT) or \
               (a == Direction.LEFT and b == Direction.UP)

    @staticmethod
    def is_rotated_counterclockwise(a: Direction, b: Direction):
        return (a == Direction.UP and b == Direction.LEFT) or \
               (a == Direction.RIGHT and b == Direction.UP) or \
               (a == Direction.DOWN and b == Direction.RIGHT) or \
               (a == Direction.LEFT and b == Direction.DOWN)

    @staticmethod
    def move(x: int, y: int, direction: Direction, height, width):
        if direction == Direction.UP:
            if y == 0:
                return x, height - 1
            else:
                return x, y - 1
        elif direction == Direction.RIGHT:
            if x == width - 1:
                return 0, y
            else:
                return x + 1, y
        elif direction == Direction.DOWN:
            if y == height - 1:
                return x, 0
            else:
                return x, y + 1
        elif direction == Direction.LEFT:
            if x == 0:
                return width - 1, y
            else:
                return x - 1, y
        else:
            print('ERROR unknown direction')
            return None


ALL_DIRECTIONS = [
    Direction.UP,
    Direction.RIGHT,
    Direction.DOWN,
    Direction.LEFT
]

# Colors
# 000000 / (0,     0,   0) (schwarz)
# 55415f / (85,   65,  95) (lila)
# 646964 / (100, 105, 100) (grau)
# d77355 / (215, 115,  85) (rot)
# 508cd7 / (80,  140, 215) (blau)
# 64b964 / (100, 185, 100) (grün)
# e6c86e / (230, 200, 110) (gelb)
# dcf5ff / (220, 245, 255) (weiß)


class Color:
    # Field color (red, green, blue)

    SNAKE_1_DEFAULT = (80,  140, 215)
    SNAKE_2_DEFAULT = (100, 185, 100)
    SNAKE_3_DEFAULT = (230, 200, 110)
    SNAKE_4_DEFAULT = (85,   65,  95)
    fruit = (215, 115,  85)
    background = (0, 0, 0)
    wall = (100, 105, 100)
