import gym
from gym import spaces
import numpy as np
from scipy.misc import imresize

from ple import PLE
from ple.games.pong import Pong


class PongEnv(gym.Env):
    def __init__(self):
        self.resize_factor = 0.5
        self.width = 64
        self.height = 48
        self.ple = PLE(game=Pong(), fps=30, frame_skip=8)
        self.action_set = self.ple.getActionSet()
        self.action_space = spaces.Discrete(len(self.action_set))
        self.observation_space = spaces.Box(
            low=0.0,
            high=255.0,
            shape=(
                int(self.width * self.resize_factor),
                int(self.height * self.resize_factor),
                1,
            ),
            dtype=np.uint32,
        )

    def reset(self):
        self.ple.display_screen = False
        self.ple.reset_game()
        return self._get_state()

    def step(self, action):
        reward = self.ple.act(self.action_set[action])
        next_state = self._get_state()
        terminal = self.ple.game_over()
        return next_state, reward, terminal, {}

    def render(self, mode="human"):
        self.ple.display_screen = True

    def _get_state(self):
        return np.expand_dims(
            imresize(self.ple.getScreenGrayscale(), self.resize_factor), axis=-1
        )
