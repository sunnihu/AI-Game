import numpy as np
import math


class LearningPolicy:

    @staticmethod
    def constant_epsilon(epsilon: float):
        """
        Epsilon never changes.
        :param epsilon:
        :return:
        """
        assert 1 >= epsilon >= 0
        def epsilon_generator():
            while True:
                yield epsilon
        return epsilon_generator()

    @staticmethod
    def linear_annealed_epsilon(epsilon_initial: float, epsilon_end: float, number_epochs: int):
        """
        Epsilon is decreased linearly from epsilon_initial to epsilon_end over number_epochs epochs
        :param epsilon_initial:
        :param epsilon_end:
        :param number_epochs:
        :return:
        """
        assert 1 >= epsilon_initial >= 0
        assert 1 >= epsilon_end >= 0
        assert epsilon_initial >= epsilon_end
        assert number_epochs > 0

        delta = (epsilon_initial - epsilon_end) / number_epochs

        def epsilon_generator():
            epsilon = epsilon_initial
            while True:
                yield epsilon
                epsilon = np.clip(epsilon - delta, epsilon_end, epsilon_initial)

        return epsilon_generator()

    @staticmethod
    def exponentially_annealed_epsilon(decay_factor: float, lower_bound: float):
        assert 1 >= lower_bound >= 0

        def epsilon_generator():
            x = 0
            while True:
                yield np.clip(math.exp(-(decay_factor * x)), lower_bound, 1.0)
                x += 1

        return epsilon_generator()