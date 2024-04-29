# -*-coding:utf-8 -*-

import tensorflow as tf

TRAIN_PARAMS = {
    'dtype': tf.float32,
    'lr': 5e-4,
    'log_steps': 10,
    'pretrain_dir': './pretrain_model/ch_google',  # pretrain Bert-Model
    'batch_size': 8,
    'epoch_size': 5,
    'embedding_dropout': 0.1,
    'warmup_ratio': 0.1,
    'early_stop_ratio': 1  # stop after ratio * steps_per_epoch
}

RUN_CONFIG = {
    'summary_steps': 10,
    'log_steps': 10,
    'save_steps': 500,
    'keep_checkpoint_max': 3,
    'allow_growth': True,
    'pre_process_gpu_fraction': 0.8,
    'log_device_placement': True,
    'allow_soft_placement': True,
    'inter_op_parallel': 2,
    'intra_op_parallel': 2
}

PATH = 'D:/data/ChineseNER'

model_api = {"bilstm_crf_softlexicon_msra": "8500",
             "bert_bilstm_crf_softlexicon_maritime": "8400"}
