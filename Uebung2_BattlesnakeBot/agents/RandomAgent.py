from .BaseAgent import BaseAgent
from environment.game import Game
from environment.models.snake import Snake
import numpy as np
from environment.models.grid_map import GridMap


class RandomAgent(BaseAgent):

    def act(self, game: Game, snake_idx: int):
        snake = game.get_snake(snake_idx)
        possible_actions = snake.possible_actions()

        if possible_actions is None:
            return None

        grid_map = game.get_grid()

        busy_action = self.feel_busy(snake, game, grid_map)
        if busy_action is not None:
            return busy_action

        return np.random.choice(possible_actions)

    def feel_busy(self, snake: Snake, game: Game, grid_map: GridMap):

        possible_actions = snake.possible_actions()
        head = snake.get_head()

        if possible_actions is None:
            return None

        actions_without_obstacle = []

        for action in possible_actions:
            neighbor = grid_map.get_neighbor(head.x, head.y, action)

            if neighbor is None:
                continue

            if not Game.is_obstacle(neighbor):
                actions_without_obstacle.append(action)

        if len(actions_without_obstacle) > 0:
            return np.random.choice(actions_without_obstacle)
        else:
            return None

    def get_name(self, snake_idx: int):
        return 'RandomSnake ' + str(snake_idx + 1)