import typing

import numpy as np


class UCTNode:
    def __init__(
        self,
        state: np.ndarray,
        active_player: int,
        action: int,
        num_actions: int,
        valid_actions: np.ndarray,
        parent: typing.Optional["UCTNode"] = None,
    ):
        self.state = state
        self.active_player = active_player
        self.action = action
        self.parent = parent
        self.is_leaf = True
        self.children = {}
        self.num_actions = num_actions
        self.valid_actions = valid_actions
        self.child_values = np.zeros(shape=(num_actions,), dtype=np.float32)
        self.child_visits = np.zeros(shape=(num_actions,), dtype=np.float32)

    @property
    def visits(self):
        if self.parent:
            return self.parent.child_visits[self.action]
        else:
            return np.sum(self.child_visits)

    @visits.setter
    def visits(self, visits):
        self.parent.child_visits[self.action] = visits

    @property
    def value(self):
        if self.parent:
            return self.parent.child_values[self.action]
        else:
            return np.sum(self.child_values)

    @value.setter
    def value(self, value):
        self.parent.child_values[self.action] = value

    @property
    def state_for_player(self):
        return self.state * self.active_player

    def policy(self):
        action_probabilties = self.child_visits * self.valid_actions
        action_probabilties /= np.sum(action_probabilties)
        return action_probabilties

    def select(self, env, c: float = np.sqrt(2)):
        # raise Exception("Hier Select-Phase aus Aufgabe 2 implementieren")

        current_node = self
        env.reset(current_node.state, current_node.active_player)

        while not current_node.is_leaf:

            best_action = np.argmax(current_node.uct(c))
            if best_action not in current_node.children:
                env.reset(current_node.state, current_node.active_player)
                env.step(best_action)
                current_node.children[best_action] = UCTNode(
                    state=env.get_state(),
                    active_player=env.get_active_player(),
                    action=best_action,
                    num_actions=self.num_actions,
                    valid_actions=env.get_valid_actions(),
                    parent=current_node,
                )

            current_node = current_node.children[best_action]

        return current_node, env.get_outcome()

    def expand(self):
        # raise Exception("Hier Expand-Phase aus Aufgabe 2 implementieren")
        self.is_leaf = False

    def simulate(self, env):
        """
        Simuliert ein zufälliges Spiel

        :param env:
        :return: outcome des Spiels
        """
        # raise Exception("Hier Simulate-Phase aus Aufgabe 2 implementieren")
        leaf_node = self
        env.reset(leaf_node.state, leaf_node.active_player)
        outcome = env.get_outcome()
        while outcome is None:
            valid_act = env.get_valid_actions()
            valid_index = np.where(valid_act == 1)[0]
            random_i = np.random.choice(valid_index)
            # print(np.where(valid_act == 1))
            env.step(random_i)
            outcome = env.get_outcome()

        return outcome

    def backup(self, winner: int):
        # raise Exception("Hier Backup-Phase aus Aufgabe 2 implementieren")
        current_node = self
        while current_node.parent is not None:
            if winner == current_node.parent.active_player:
                current_node.value += 1
            current_node.visits += 1
            current_node = current_node.parent

    def uct(self, c: float):

        # raise Exception("Hier UCB aus Aufgabe 2 implementieren")
        invalid_act = 1 - self.valid_actions
        invalid_act = invalid_act * 1000
        uct = self.child_values/(self.child_visits + 1) + c/(self.child_visits + 1) * np.sqrt(np.log(self.visits + 1))
        return uct - invalid_act
