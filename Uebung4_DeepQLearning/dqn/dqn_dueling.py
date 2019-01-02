from typing import Tuple, Union

import keras
from keras.layers import Dense, Input, Lambda
import tensorflow as tf

from .dqn import encode


def make_dqn_dueling(
    input_shape: Union[Tuple[int], Tuple[int, int, int]],
    hidden_dim: int,
    num_actions: int,
):
    # raise Exception("Hier Aufgabe 4 implementieren")
    # shape: input_shape
    input_observations = Input(shape=input_shape)
    # shape: (num_actions,)
    input_actions = Input(shape=(num_actions,))

    encoded = encode(input_observations, input_shape, hidden_dim)

    # shape: (num_actions,)
    advantage = Dense(num_actions)(Dense(265, activation='relu')(encoded))

    # shape: (1,)
    value = Dense(1)(Dense(265, activation='relu')(encoded))
    a_mean = Lambda(lambda x: - keras.backend.mean(x, axis=-1))(advantage)
    output = keras.layers.Add()([value, advantage, a_mean])

    masked_output = keras.layers.Multiply()([output, input_actions])
    model = keras.Model(
        inputs=[input_observations, input_actions], outputs=masked_output
    )
    return model

