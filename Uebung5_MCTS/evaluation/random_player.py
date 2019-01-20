import random
import numpy as np

from environment.connect_four import ConnectFour


class RandomPlayer:

    def __init__(
        self, player: int, simulation_env: ConnectFour
    ):
        self.simulation_env = simulation_env
        self.player = player

    def act(self, state: np.ndarray):
        self.simulation_env.reset(state, self.player)
        valid_actions = list(self.simulation_env.get_valid_actions().nonzero()[0])
        return random.sample(valid_actions, k=1)