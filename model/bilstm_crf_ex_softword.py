# -*-coding:utf-8 -*-
from tools.train_utils import *
from tools.layer import *
from tools.utils import add_layer_summary
from config import TRAIN_PARAMS


def build_graph(features, labels, params, is_training):
    """
    Giga pretrain character embedding+  bilstm + CRF + ex_softword word enhance
    """
    input_ids = features['token_ids']
    label_ids = features['label_ids']

    seq_len = features['seq_len']
    ex_softword_ids = features['ex_softword_ids']  # bathc * ma_seq * word_enhance_dim
    ex_softword_ids = tf.reshape(ex_softword_ids, [-1, params['max_seq_len'], params['word_enhance_dim']])

    with tf.variable_scope('embedding'):
        embedding = tf.nn.embedding_lookup(params['embedding'], input_ids)
        embedding = tf.layers.dropout(embedding, rate=params['embedding_dropout'],
                                      seed=1234, training=is_training)
        add_layer_summary(embedding.name, embedding)

    with tf.variable_scope('word_enhance'):
        emb_dim = embedding.shape.as_list()[-1]  # 默认和char emb相同，向量可加可拼接
        softword_embedding = tf.get_variable(
            shape=[params['word_enhance_dim'], emb_dim],
            initializer=tf.truncated_normal_initializer(), name='ex_softword_embedding')
        wh_embedding = tf.matmul(ex_softword_ids, softword_embedding)  # max_seq_len * emb_dim
        add_layer_summary('ex_softword', softword_embedding)
        wh_embedding = tf.layers.dropout(wh_embedding, rate=params['embedding_dropout'],
                                         seed=1234, training=is_training)
        embedding = tf.concat([wh_embedding, embedding], axis=-1)  # concat word enhance with token embedding

    lstm_output = bilstm(embedding, params['cell_type'], params['rnn_activation'],
                         params['hidden_units_list'], params['keep_prob_list'],
                         params['cell_size'], seq_len, params['dtype'], is_training)

    lstm_output = tf.layers.dropout(lstm_output, seed=1234, rate=params['embedding_dropout'],
                                    training=is_training)

    logits = tf.layers.dense(lstm_output, units=params['label_size'], activation=None,
                             use_bias=True, name='logits')
    add_layer_summary(logits.name, logits)

    trans, log_likelihood = crf_layer(logits, label_ids, seq_len, params['label_size'], is_training)
    pred_ids = crf_decode(logits, trans, seq_len, params['idx2tag'], is_training)
    crf_loss = tf.reduce_mean(-log_likelihood)

    return crf_loss, pred_ids


RNN_PARAMS = {
    'cell_type': 'lstm',
    'cell_size': 1,
    'hidden_units_list': [128],
    'keep_prob_list': [1],
    'rnn_activation': 'tanh'
}

TRAIN_PARAMS.update(RNN_PARAMS)
TRAIN_PARAMS.update({

    'lr': 0.005,
    'decay_rate': 0.95,  # lr * decay_rate ^ (global_step / train_steps_per_epoch)
    'embedding_dropout': 0.3,
    'early_stop_ratio': 1  # stop after no improvement after 1.5 epochs
})
