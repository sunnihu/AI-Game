import gym

import numpy as np
from rendering.interface import Interface


class ConnectFour(gym.Env):
    def __init__(self, num_rows: int, num_columns: int):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.board = np.zeros(shape=(self.num_rows, self.num_columns), dtype=np.int8)
        self.active_player = 1 if np.random.uniform(0.0, 1.0) < 0.5 else -1
        self.interface = Interface(self.board)

    def reset(self, state: np.ndarray, active_player: int):
        self.board = np.copy(state)
        self.active_player = active_player

    def step(self, action: int):
        if self.get_valid_actions()[action] == 0:
            self.render()
            print("Invalid action")
        action_row = -1
        for row in range(self.num_rows):
            if self.board[row, action] == 0:
                action_row = row
        if action_row >= 0:
            self.board[action_row, action] = self.active_player
            self.active_player = -self.active_player

    def render(self, mode="human"):
        if mode == "ansi":
            return print(str(self.board))
        elif mode == "human":
            self.interface.render(self.board)

    def get_valid_actions(self):
        """
        Gibt eine Maske zurück, welche Aktionen gewählt werden können
        :return:
        """
        return np.array(
            [
                (1 if self.board[0, column] == 0 else 0)
                for column in range(self.num_columns)
            ]
        )

    def get_num_actions(self):
        return self.num_columns

    def get_active_player(self):
        return self.active_player

    def get_outcome(self):
        for player in [-1, 1]:
            for j in range(self.num_rows - 3):
                for i in range(self.num_columns):
                    if (
                        self.board[j, i] == player
                        and self.board[j + 1, i] == player
                        and self.board[j + 2, i] == player
                        and self.board[j + 3, i] == player
                    ):
                        return player

            for i in range(self.num_columns - 3):
                for j in range(self.num_rows):
                    if (
                        self.board[j, i] == player
                        and self.board[j, i + 1] == player
                        and self.board[j, i + 2] == player
                        and self.board[j, i + 3] == player
                    ):
                        return player

            for i in range(self.num_columns):
                for j in range(self.num_rows - 3):
                    if (
                        self.board[j, i] == player
                        and self.board[j + 1, i - 1] == player
                        and self.board[j + 2, i - 2] == player
                        and self.board[j + 3, i - 3] == player
                    ):
                        return player

            for i in range(3, self.num_columns):
                for j in range(3, self.num_rows):
                    if (
                        self.board[j, i] == player
                        and self.board[j - 1, i - 1] == player
                        and self.board[j - 2, i - 2] == player
                        and self.board[j - 3, i - 3] == player
                    ):
                        return player
        if np.sum(self.get_valid_actions()) > 0:
            return None
        else:
            return 0

    def get_state(self):
        return self.board
