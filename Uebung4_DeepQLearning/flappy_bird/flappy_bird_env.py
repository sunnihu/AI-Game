import gym
from gym import spaces
import numpy as np
from scipy.misc import imresize

from ple import PLE
from ple.games.flappybird import FlappyBird


class FlappyBirdEnv(gym.Env):
    def __init__(self):
        self.resize_factor = 0.125
        self.width = 288
        self.height = 512
        self.ple = PLE(game=FlappyBird(), fps=30, frame_skip=8)
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
        self._steps = 0

    def reset(self):
        self._steps = 0
        self.ple.display_screen = False
        self.ple.reset_game()
        return self._get_state()

    def step(self, action):
        self._steps += 1
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
