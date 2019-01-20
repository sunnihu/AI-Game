import numpy as np


def evaluate(state: np.ndarray):
    """
    Evaluates a given state and returns its estimated winner in [-1, 1].
    """
    # raise Exception("Hier Aufgabe 1 implementieren")
    score = 0
    s1 = np.array([1, 1, 1, 1])
    s_1 = np.array([-1, -1, -1, -1])
    tmp = np.zeros(state.shape)

    for i in range(state.shape[0]):
        row = state[i, :]
        idx = np.where(row == 1)[0]
        pos_ones = np.split(row[idx], np.where(np.diff(idx) != 1)[0]+1)[0]
        idx = np.where(row == -1)[0]
        neg_ones = np.split(row[idx], np.where(np.diff(idx) != 1)[0]+1)[0]

        if np.array_equal(pos_ones, s1):
            score += 1
        if np.array_equal(neg_ones, s_1):
            score += -1


    for j in range(state.shape[1]):
        col = state[:, j]
        idx = np.where(col == 1)[0]
        pos_ones = np.split(col[idx], np.where(np.diff(idx) != 1)[0]+1)[0]
        idx = np.where(col == -1)[0]
        neg_ones = np.split(col[idx], np.where(np.diff(idx) != 1)[0]+1)[0]

        if np.array_equal(pos_ones, s1):
            score += 1
        if np.array_equal(neg_ones, s_1):
            score += -1

    return score

