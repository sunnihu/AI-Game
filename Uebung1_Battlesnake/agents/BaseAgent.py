from abc import abstractmethod
from environment.game import Game
from environment.models.game_object import GameObject
from environment.models.constants import Direction
from environment.models.wall import Wall
from environment.models.fruit import Fruit
from environment.models.empty_field import EmptyField
from environment.models.snake import SnakePart


class BaseAgent:

    def __init__(self):
        self._color = None

    @abstractmethod
    def get_name(self, snake_idx: int):
        pass

    def get_color(self):
        return self._color

    def user_key_pressed(self, key):
        pass

    @abstractmethod
    def act(self, state: Game, snake_idx: int):
        pass

    @staticmethod
    def direction_to_reach_field(current_field: GameObject, field: GameObject):

        delta_x = current_field.x - field.x
        delta_y = current_field.y - field.y

        if abs(delta_x) > abs(delta_y):
            # horizontale Bewegung

            if delta_x > 0:
                return Direction.LEFT
            else:
                return Direction.RIGHT
        else:
            if delta_y > 0:
                return Direction.UP
            else:
                return Direction.DOWN

