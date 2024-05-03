# -*-coding:utf-8 -*-

import tensorflow as tf

TRAIN_PARAMS = {
    'dtype': tf.float32,
    'lr': 5e-4,
    'log_steps': 10,
    'pretrain_dir': './pretrain_model/ch_google',  # pretrain Bert-Model
    'batch_size': 8,
    'epoch_size': 5,
    'embedding_dropout': 0.5,
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
             "bert_bilstm_crf_softlexicon_maritime": "8400",
             "bert_bilstm_crf_msra": "8300"}

# 此处仅做绘制混淆矩阵使用，具体tag去data-dataset查看
MARITIME = {
    'B-CORP': 2,
    'I-CORP': 3,
    'B-CW': 4,
    'I-CW': 5,
    'B-GRP': 6,
    'I-GRP': 7,
    'B-LOC': 8,
    'I-LOC': 9,
    'B-PER': 10,
    'I-PER': 11,
    'B-PROD': 12,
    'I-PROD': 13,
}
