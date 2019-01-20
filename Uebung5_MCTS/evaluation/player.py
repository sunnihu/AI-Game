import numpy as np

from environment.connect_four import ConnectFour
from evaluation.evaluate import evaluate


class Player:
    def __init__(
        self, player: int, simulation_env: ConnectFour
    ):
        self.simulation_env = simulation_env
        self.player = player

    def act(self, state: np.ndarray):
        self.simulation_env.reset(state, self.player)
        valid_actions = self.simulation_env.get_valid_actions().nonzero()[0]
        values = np.zeros_like(valid_actions, dtype=np.float)
        for idx, action in enumerate(valid_actions):
            self.simulation_env.step(action)
            next_state = self.simulation_env.get_state()
            value = evaluate(next_state)
            # Multiply with self.player (-1 or 1) so we can always choose the argmax
            values[idx] = value * self.player
            self.simulation_env.reset(state, self.player)
        return valid_actions[np.argmax(values)]
