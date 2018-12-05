import numpy as np
import random
from .BaseAgent import BaseAgent


class RandomAgent(BaseAgent):

    def get_action(self, state, possible_actions):
        action = random.choice(possible_actions)
        return action

    def update(self, state, action, reward, next_state, next_state_possible_actions, done):
        pass

    def reset(self):
        pass

    def to_dictionary(self):
        pass

    def get_q__values(self):
        return None