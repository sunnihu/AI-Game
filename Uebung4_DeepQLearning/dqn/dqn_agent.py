from typing import List, NamedTuple

import keras
import numpy as np

from exploration import ExplorationStrategy
from replay_memory import ReplayMemory, Transition

from .huber_loss import huber_loss


class HyperParameters(NamedTuple):
    learning_rate: float
    gamma: float


class DQNAgent:

    """
    Reinforcement Learning Agent that uses a DQN.

    See https://arxiv.org/abs/1312.5602
    """

    def __init__(
        self,
        dqn: keras.Model,
        replay_memory: ReplayMemory,
        exploration_strategy: ExplorationStrategy,
        hyper_parameters: HyperParameters,
        num_actions: int,
        output_dir: str,
    ):
        self.global_step = 0
        self.episode = 0
        self.hyper_parameters = hyper_parameters
        self.num_actions = num_actions
        self.output_dir = output_dir

        self.dqn = dqn
        self.optimizer = keras.optimizers.Adam(lr=hyper_parameters.learning_rate)
        self.dqn.compile(loss=huber_loss, optimizer=self.optimizer)
        self.dqn.summary()
        self.replay_memory = replay_memory
        self.exploration_strategy = exploration_strategy

    def act(self, state):
        """
        Use the DQN to choose an action for the given state.

        Arguments:
            state {`np.ndarray`} -- Tensor representation of the state

        Returns:
            `int` -- Index of the chosen action
        """
        self.global_step += 1
        is_convolutional = len(self.dqn.input_shape[0]) == 4
        state = np.array(state)
        if is_convolutional:
            if len(state.shape) == 3:
                state = np.expand_dims(state, 0)
            state = state / 255.0
        else:
            if len(state.shape) == 1:
                state = np.expand_dims(state, 0)
        q_values = np.squeeze(
            self.dqn.predict([state, np.ones(shape=(1, self.num_actions))])
        )
        return self.exploration_strategy.choose_action(q_values, self.episode)

    def observe(self, transition: Transition):
        self.replay_memory.add(transition)
        if transition.next_state is None:
            self.episode += 1

    def train(self):
        """
        Sample a batch of transitions and update the DQN using gradient descent.

        Returns:
            `float` -- Mean loss for the sampled training batch
        """
        if not self.replay_memory.filled():
            return

        transitions = self.replay_memory.sample()
        tensors = self._get_tensors(transitions)
        loss = self._compute_loss(*tensors)

        if self.global_step % 1000 == 0:
            self.dqn.save_weights("{}/checkpoint.h5".format(self.output_dir))

        return loss

    def _compute_loss(
        self,
        state_tensor,
        action_tensor,
        reward_tensor,
        next_state_tensor,
        non_terminal_mask,
    ):
        """
        Compute the Q-Learning loss for the DQN.

        Arguments:
            state_tensor {`np.ndarray`} -- Tensor of states
            action_tensor {`np.ndarray`} -- Tensor of the chosen actions
            reward_tensor {`np.ndarray`} -- Tensor of the observed rewards
            next_state_tensor {`np.ndarray`} -- Tensor of the next states
            non_terminal_mask {`np.ndarray`} -- Tensor indicating the non-terminal states

        Returns:
            `float` -- Loss 
        """
        batch_size = state_tensor.shape[0]
        q_values_next = self.dqn.predict(
            [next_state_tensor, np.ones(shape=(batch_size, self.num_actions))]
        )
        q_values_next_max = np.zeros(shape=(batch_size,))
        q_values_next_max[non_terminal_mask] = np.max(q_values_next, axis=-1)

        q_values_target = np.zeros(shape=(batch_size, self.num_actions))

        for i in range(batch_size):
            q_values_target[i, action_tensor[i]] = (
                reward_tensor[i] + self.hyper_parameters.gamma * q_values_next_max[i]
            )

        actions_one_hot = np.eye(self.num_actions)[action_tensor]

        return self._fit(x=[state_tensor, actions_one_hot], y=q_values_target)

    def _fit(self, x: np.ndarray, y: np.ndarray):
        """
        Performs one epoch of supervised training of the DQN.
        
        Arguments:
            x {np.ndarray} -- input
            y {np.ndarray} -- target output
        
        Returns:
            `float` -- Loss
        """
        history = self.dqn.fit(x=x, y=y, epochs=1, verbose=0)
        return history.history["loss"][0]

    def _get_tensors(self, transitions: List[Transition]):
        """
        Transform the transitions into Pytorch tensors for training.

        Arguments:
            transitions {`List[Transition]`} -- Sampled transition batch

        Returns:
            `Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]` -- Tensors to be used for training
        """
        state_tensor = np.array([np.array(t.state) for t in transitions])
        action_tensor = np.array([t.action for t in transitions], dtype=np.int64)
        reward_tensor = np.array([t.reward for t in transitions])
        next_state_tensor = np.array(
            [np.array(t.next_state) for t in transitions if t.next_state is not None]
        )

        non_terminal_mask = np.array(
            [t.next_state is not None for t in transitions], dtype=np.uint8
        ).nonzero()
        return (
            state_tensor,
            action_tensor,
            reward_tensor,
            next_state_tensor,
            non_terminal_mask,
        )
