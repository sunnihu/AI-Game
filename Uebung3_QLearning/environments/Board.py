import numpy as np
from typing import List
from settings import Action, FieldType


class Position:
    def __init__(self,
                 x: int,
                 y: int):
        self.x = x
        self.y = y

    def after_action(self, action: Action) -> 'Position':
        return Position(self.x + action.value[0], self.y + action.value[1])


class Board:

    def __init__(self,
                 width: int,
                 height: int,
                 blocked_positions: List[Position],
                 end_positions: List[Position],
                 end_rewards: List[float],
                 default_reward: float = None,
                 position: Position = None):

        self.width = width
        self.height = height
        self.end_positions = end_positions
        self.blocked_positions = blocked_positions
        self.default_reward = default_reward
        self.end_rewards = end_rewards

        # ordered like this, because board can be easily printed for debugging purposes
        self.board = np.zeros(shape=(2, height, width), dtype=np.float32)

        for index, end in enumerate(end_positions):
            self.board[0][end.y][end.x] = FieldType.END_POS
            self.board[1][end.y][end.x] = end_rewards[index]

        for blocked in blocked_positions:
            self.board[0][blocked.y][blocked.x] = FieldType.BLOCKED

        self.position = position

    def get_state(self) -> int:
        return self.position.y * self.width + self.position.x

    def possible_actions(self) -> List[Action]:
        actions = []
        for action in [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]:
            if self.is_valid_action(action):
                actions.append(action)
        return actions

    def random_free_position(self) -> Position:
        # we choose one index of all free positions randomly, no end position!
        y, x = np.where(self.board[0][:][:] == FieldType.EMPTY)
        i = np.random.randint(len(x))
        return Position(x[i], y[i])

    def is_free_position(self, pos: Position) -> bool:
        # position is not blocked and no end position
        return self.is_valid_position(pos) and self.field_type_at_position(pos) == FieldType.EMPTY

    def is_valid_position(self, pos: Position) -> bool:
        # position inside board coordinates and not blocked
        return (0 <= pos.x < self.width) and (0 <= pos.y < self.height) and self.field_type_at_position(pos) != FieldType.BLOCKED

    def is_valid_action(self, action: Action) -> bool:
        return self.is_valid_position(self.position.after_action(action))

    def field_type_at_position(self, position: Position):
        return self.board[0][position.y][position.x]

    def perform_action(self, action: Action) -> (int, float, bool):
        """
        Carries out action when possible
        :param action: action of type Action
        :return: reward, state, done after action is performed
        """
        if self.is_valid_action(action):
            self.position = self.position.after_action(action)
            if self.field_type_at_position(self.position) == FieldType.END_POS:
                return self.get_state(), self.board[1][self.position.y][self.position.x], True
            else:
                return self.get_state(), self.default_reward, False
        else:
            raise Exception(f"Action {action.name} cannot be performed at position {self.position.x, self.position.y}, because the next position seems to be invalid!")