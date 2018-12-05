from .BaseAgent import BaseAgent
from typing import List
from environments.Board import Action
import math
import numpy as np


class QLearningAgent(BaseAgent):

    def __init__(self,
                 alpha: float,
                 epsilon_policy,
                 discount: float,
                 action_space: List[Action],
                 state_space: int,
                 q_values: np.ndarray = None):

        super().__init__(action_space, state_space)

        self.alpha = alpha
        self.epsilon = 1.0
        self.epsilon_policy = epsilon_policy
        self.discount = discount
        self.action_space = action_space
        self.state_space = state_space

        if q_values is None:
            # init with zeros
            self.q_values = np.zeros((state_space, len(action_space)), np.float32)
        else:
            self.q_values = q_values

    def get_q__values(self) -> np.ndarray:
        return self.q_values

    def get_best_action(self, state: int, possible_actions: List[Action]) -> (float, Action):

        if len(possible_actions) == 0:
            raise Exception("Agent is stuck and can not move! Check if the map makes sense.")

        best_value = -math.inf
        best_actions = []

        # if two actions have the same Q value, choose a random one
        for action in possible_actions:
            q_value = self.q_values[state][self.action_space.index(action)]
            if q_value > best_value:
                best_value = q_value
                best_actions = [action]
            elif q_value == best_value:
                best_actions.append(action)

        return best_value, np.random.choice(best_actions)

    def get_action(self, state: int, possible_actions: List[Action]) -> Action:
        # raise Exception("Hier Aufgabe 3.1 implementieren")
        # pass
        p = np.random.random_sample()
        if p < self.epsilon:
            return np.random.choice(possible_actions)
        else:
            best_value, best_action = self.get_best_action(state, possible_actions)
            return best_action

    def update(self,
               state : int,
               action : Action,
               reward : float, next_state : int,
               next_state_possible_actions : List[Action],
               done : bool):

        # raise Exception("Hier Aufgabe 3.2 implementieren")
        # pass
        q_value = self.q_values[state][self.action_space.index(action)]
        next_best_value, next_best_action = self.get_best_action(next_state, next_state_possible_actions)
        q_new = (1 - self.alpha) * q_value + self.alpha * (reward + self.discount * next_best_value)
        if not done:
            self.q_values[state][self.action_space.index(action)] = q_new
        else:
            q_new = (1 - self.alpha) * q_value + self.alpha*reward
            self.q_values[state][self.action_space.index(action)] = q_new

    def reset(self):
        self.q_values = np.zeros((self.state_space, len(self.action_space)), np.float32)

    def to_dictionary(self):
        state = {"q_values": self.q_values.tolist(),
                 "epsilon": self.epsilon,
                 "alpha": self.alpha,
                 "discount": self.discount,
                 "state_space": self.state_space}

        return state