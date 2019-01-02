from typing import Tuple, Union

import keras
from keras.layers import Dense, Input


def encode(
    input_observations: keras.layers.Input,
    input_shape: Union[Tuple[int], Tuple[int, int, int]],
    hidden_dim: int,
):
    if len(input_shape) == 1:
        # 1-dimensional states
        encoded = keras.layers.Dense(
            units=hidden_dim, activation="relu", name="encoder/dense1"
        )(input_observations)
        encoded = keras.layers.Dense(
            units=hidden_dim, activation="relu", name="encoder/dense2"
        )(encoded)
    else:
        # 2-dimensional states (e.g. images)
        encoded = keras.layers.Conv2D(
            filters=16,
            kernel_size=8,
            strides=4,
            padding="same",
            input_shape=input_shape,
            activation="relu",
            name="encoder/conv1",
        )(input_observations)
        encoded = keras.layers.Conv2D(
            filters=32,
            kernel_size=4,
            strides=2,
            padding="same",
            input_shape=input_shape,
            activation="relu",
            name="encoder/conv2",
        )(encoded)
        encoded = keras.layers.Conv2D(
            filters=32,
            kernel_size=3,
            strides=1,
            padding="same",
            input_shape=input_shape,
            activation="relu",
            name="encoder/conv3",
        )(encoded)
        encoded = keras.layers.Flatten()(encoded)
        encoded = keras.layers.Dense(units=hidden_dim, activation="relu")(encoded)
    return encoded


def make_dqn(
    input_shape: Union[Tuple[int], Tuple[int, int, int]],
    hidden_dim: int,
    num_actions: int,
):
    # Exception("Hier Aufgabe 2 implementieren")
    # shape: input_shape
    input_observations = Input(shape=input_shape)
    # shape: (num_actions,)
    input_actions = Input(shape=(num_actions,))

    encoded = encode(input_observations, input_shape, hidden_dim)

    # shape: (num_actions,)
    output = Dense(num_actions)(encoded)

    masked_output = keras.layers.Multiply()([output, input_actions])
    model = keras.Model(
        inputs=[input_observations, input_actions], outputs=masked_output
    )
    return model
