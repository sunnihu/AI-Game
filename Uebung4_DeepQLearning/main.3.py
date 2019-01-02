import random

import numpy as np
import tensorflow as tf

from main import main

if __name__ == "__main__":
    SEED = 42
    random.seed(SEED)
    tf.set_random_seed(SEED)
    np.random.seed(SEED)
    main("Aufgabe-3")
