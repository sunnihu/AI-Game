from abc import abstractmethod
import numpy as np
from environments.Board import Action
from typing import List


class BaseAgent:

    def __init__(self, action_space, state_space):
        self.action_space = action_space
        self.state_space = state_space

    @abstractmethod
    def get_action(self, state: int, possible_actions: List[Action]) -> Action:
        pass

    @abstractmethod
    def update(self, state: int, action: Action, reward: float, next_state: int, next_state_possible_actions: List[Action], done: bool):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def to_dictionary(self):
        pass