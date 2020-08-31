import tensorflow as tf


def load_model(graph: tf.Graph, sess: tf.Session, path: str):
    with sess.as_default():
        with graph.as_default():
            saver = tf.train.Saver()
            saver.restore(sess, tf.train.latest_checkpoint(path))
