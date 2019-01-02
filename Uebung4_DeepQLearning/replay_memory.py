import random
from collections import deque
from typing import List, NamedTuple

import numpy as np


class Transition(NamedTuple):
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray


class ReplayMemory:

    """
    Memory of transitions from which the DQN can be trained.
    """

    def __init__(self, max_size: int, batch_size: int):
        self.buffer = deque([], max_size)
        self.batch_size = batch_size

    def filled(self):
        return len(self.buffer) > self.batch_size

    def add(self, transition: Transition):
        self.buffer.append(transition)

    def sample(self) -> List[Transition]:
        return random.sample(self.buffer, self.batch_size)
        