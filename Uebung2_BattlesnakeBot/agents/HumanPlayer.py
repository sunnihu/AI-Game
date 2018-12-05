from .BaseAgent import BaseAgent
from environment.game import Game
from environment.models.constants import Direction
from pygame.locals import *


class HumanPlayer(BaseAgent):

    def __init__(self):
        super().__init__()

        self.next_action = Direction.RIGHT
        self.last_action = Direction.RIGHT

    def user_key_pressed(self, key):

        if key == K_UP:
            self.next_action = Direction.UP
        elif key == K_DOWN:
            self.next_action = Direction.DOWN
        elif key == K_LEFT:
            self.next_action = Direction.LEFT
        elif key == K_RIGHT:
            self.next_action = Direction.RIGHT

    def act(self, game: Game, snake_idx: int):
        snake = game.get_snake(snake_idx)
        possible_actions = snake.possible_actions()

        if self.next_action in possible_actions:
            self.last_action = self.next_action

        return self.last_action

    def get_name(self, snake_idx: int):
        return 'Human Player'
