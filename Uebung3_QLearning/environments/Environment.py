from typing import List
from environments.GameRenderer import GameRenderer
from environments.Board import Board, Action, Position
import numpy as np

class Environment:

    def __init__(
            self,
            board: Board,
            start_position: Position
    ):
        self.board = board
        self.start_position = start_position

        self.state_space = self.board.width * self.board.height
        self.action_space = [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]

        self.renderer = GameRenderer(self.board.width, self.board.height)

        # largest absolute value of all rewards in the environment, this is used to determine the arrow colors in GameRenderer
        largest_end_reward = max([abs(reward) for reward in board.end_rewards])
        self.max_abs_reward_value = max(largest_end_reward, abs(board.default_reward))

    def get_current_state(self) -> int:
        return self.board.get_state()

    def get_possible_actions(self) -> List[Action]:
        return self.board.possible_actions()

    def step(self, action: Action) -> (int, float, bool):
        return self.board.perform_action(action)

    def reset_position(self):
        if self.start_position is None:
            self.board.position = self.board.random_free_position()
        else:
            self.board.position = self.start_position

    def reset(self):
        self.reset_position()

    def render(self, q_values: np.ndarray = None, finish_state: bool = False):
        self.renderer.render(self, q_values, finish_state)
