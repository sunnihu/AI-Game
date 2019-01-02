import tensorflow as tf


def huber_loss(y_true, y_pred):
    """
    Loss function that acts like l2 loss when the absolute error is smaller than 1.0
    and as l1 loss otherwise to limit the size of the gradients.
    """

    err = y_true - y_pred

    cond = tf.abs(err) < 1.0
    L2 = 0.5 * tf.square(err)
    L1 = tf.abs(err) - 0.5

    loss = tf.where(cond, L2, L1)

    return tf.reduce_mean(loss)
