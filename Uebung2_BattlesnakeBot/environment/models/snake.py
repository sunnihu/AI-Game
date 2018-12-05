import numpy as np
from typing import List
from environment.models.constants import Direction, ALL_DIRECTIONS, DirectionUtil
from environment.models.game_object import GameObject


class SnakePart(GameObject):
    """
    Einzelnes Segment einer Schlange
    """
    def __init__(self, x: int, y: int, direction: Direction):
        super().__init__(x, y)
        self.direction = direction

class Snake:
    """
    Diese Klasse beschreibt eine Schlange, die aus mehreren SnakePart Objekten besteht.
    """
    def __init__(self, x: int, y: int):
        """
        Erzeugt eine Schlange an der gegebenen Position
        :param x: x-Koordinate der Schlange
        :param y: y-Koordinate der Schlange
        """
        self.health = 100
        head_direction: Direction = np.random.choice(ALL_DIRECTIONS)
        head = SnakePart(x, y, head_direction)
        self.body: List[SnakePart] = [head]
        self.max_length = 10
        self.color = None
        self.name = None

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_health(self):
        return self.health

    def get_head(self):
        return self.get_body_part(0)

    def get_tail(self):
        return self.get_body_part(self.length() - 1)

    def get_body_part(self, idx)-> SnakePart:
        if 0 <= idx < len(self.body):
            return self.body[idx]

        return None

    def length(self):
        return len(self.body)

    def has_full_length(self):
        return self.length() == self.max_length

    def move_head(self, move_direction):
        """
        Bewegt den den Kopf der Schlange in die Richtung von move_direction
        :param move_direction: Typ Direction (definiert in constants.py)
        :return:
        """
        self.health -= 1

        if self.is_dead():
            if self.body:
                self.die()
            return

        next_head = self._get_next_head(move_direction)

        self.body.insert(0, next_head)

        if len(self.body) > self.max_length:
            self.body.pop()

    def ate_fruit(self):
        self.max_length += 1
        self.health = 100

    def is_dead(self):
        return self.health <= 0

    def die(self):
        self.health = 0
        self.body = []

    def _get_next_head(self, direction):
        head = self.get_head()

        moved_x, moved_y = DirectionUtil.move(head.x, head.y, direction)
        return SnakePart(moved_x, moved_y, direction)

    def possible_actions(self):
        """
        Gibt alle erlaubten Richtungen zurück, in die sich die Schlange bewegen darf
        :return: Typ Direction (definiert in constants.py)
        """
        head = self.get_head()
        if head is None:
            return None

        head_direction = head.direction

        if head_direction == Direction.UP:
            return [Direction.UP, Direction.RIGHT, Direction.LEFT]
        elif head_direction == Direction.RIGHT:
            return [Direction.UP, Direction.RIGHT, Direction.DOWN]
        elif head_direction == Direction.DOWN:
            return [Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        elif head_direction == Direction.LEFT:
            return [Direction.UP, Direction.DOWN, Direction.LEFT]
        else:
            print('ERROR unknown direction')
            return None
