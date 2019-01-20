from abc import ABC, abstractmethod
from typing import List

import numpy as np


class Environment(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def reset(self, state: np.ndarray, active_player: int):
        pass

    @abstractmethod
    def get_state(self) -> np.ndarray:
        pass

    @abstractmethod
    def get_valid_actions(self) -> List[int]:
        pass

    @abstractmethod
    def get_num_actions(self) -> int:
        pass

    @abstractmethod
    def get_active_player(self) -> int:
        pass

    @abstractmethod
    def step(self, action: int) -> float:
        pass

    @abstractmethod
    def get_outcome(self) -> int:
        pass

    @abstractmethod
    def render(self):
        pass
