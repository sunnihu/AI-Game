import numpy as np

from environment.connect_four import ConnectFour
from mcts.mcts import mcts


class Player:
    def __init__(
        self, player: int, simulation_env: ConnectFour, simulation_time: float
    ):
        self.simulation_env = simulation_env
        self.simulation_time = simulation_time
        self.player = player

    def act(self, state: np.ndarray):
        self.simulation_env.reset(state, self.player)
        root_node = mcts(self.simulation_time, self.simulation_env)
        policy = root_node.policy()
        action = np.argmax(policy)
        return action

