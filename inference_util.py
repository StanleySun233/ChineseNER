# -*-coding:utf-8 -*-
import grpc
import tensorflow as tf
import numpy as np
import re
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc
from tensorflow.python.framework import tensor_util

from data.base_preprocess import get_instance, extract_prefix_surfix
from data.tokenizer import TokenizerBert
from tools.infer_utils import extract_entity, fix_tokens, timer, grpc_retry


class InferHelper(object):
    def __init__(self, max_seq_len, tag2idx, model_name, version, server, timeout):
        self.model_name = model_name
        self.word_enhance, self.tokenizer_type = extract_prefix_surfix(model_name)
        self.mtl = 1 if re.search('(mtl)|(adv)', model_name) else 0  # whether is multitask
        self.proc = get_instance(self.tokenizer_type, max_seq_len, tag2idx,
                                 word_enhance=self.word_enhance, mapping=None)
        self.max_seq_len = max_seq_len
        self.tag2idx = tag2idx
        self.idx2tag = dict([(val, key) for key, val in tag2idx.items()])
        self.server = server
        self.version = version
        self.timeout = timeout
        self.channel = None
        self.stub = None
        self.init()

    def init(self):
        # This is for channel stub reuse
        self.channel = grpc.insecure_channel(self.server)
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)

    def make_request(self, feature):
        request = predict_pb2.PredictRequest()
        request.model_spec.signature_name = 'serving_default'  # set in estimator output
        request.model_spec.name = self.model_name
        request.model_spec.version.value = self.version
        tensor_proto = tensor_util.make_tensor_proto(feature, dtype=tf.string)
        request.inputs['example'].CopyFrom(tensor_proto)
        return request

    def make_feature(self, sentence):
        self.feature = self.proc.build_seq_feature(sentence)
        # fake labels and label_ids, if you want to skip this you need to modify model_fn
        self.feature['labels'] = np.zeros(shape=(self.max_seq_len,)).astype(str).tolist()
        self.feature['label_ids'] = np.zeros(shape=(self.max_seq_len,)).astype(int).tolist()

        if self.mtl:
            self.feature['task_ids'] = 1

        if self.tokenizer_type == TokenizerBert:
            # fix word piece tokenizer UNK and ##
            self.feature['tokens'] = fix_tokens(sentence, self.feature['tokens'])

        tf_example = tf.train.Example(
            features=tf.train.Features(feature=self.proc.build_tf_feature(self.feature))
        )
        return [tf_example.SerializeToString()]

    def decode_prediction(self, resp):
        res = resp.result().outputs
        pred_ids = np.squeeze(tf.make_ndarray(res['pred_ids']))  # seq label ids
        entity = extract_entity(self.feature['tokens'], pred_ids, self.idx2tag)
        return entity

    @grpc_retry()
    def _infer(self, req):
        resp = self.stub.Predict.future(req, self.timeout)
        output = self.decode_prediction(resp)
        return output

    @timer
    def infer(self, text):
        feature = self.make_feature(text)
        req = self.make_request(feature)
        output = self._infer(req)
        return output


class InferenceUtil(object):
    def __init__(self, MAX_SEQ_LEN, TAG2IDX, MODEL, VERSION, SERVER, TIMEOUT):
        self.model = InferHelper(MAX_SEQ_LEN, TAG2IDX, MODEL, VERSION, SERVER, timeout=TIMEOUT)
        self.name = MODEL
        self.tag2idx = TAG2IDX
        self.warnup = '上海海事大学'
        self.predict(self.warnup)

    def get_tag2idx(self):
        return

    def predict(self, text):
        return self.model.infer(text)


def get_bilstm_crf_softlcion_msra():
    MODEL = 'bilstm_crf_softlexicon_msra'
    SERVER = 'localhost:8500'
    VERSION = 1
    MAX_SEQ_LEN = 150
    TIMEOUT = 10
    TAG2IDX = {
        '[PAD]': 0,
        'O': 1,
        'B-ORG': 2,
        'I-ORG': 3,
        'B-PER': 4,
        'I-PER': 5,
        'B-LOC': 6,
        'I-LOC': 7,
        '[CLS]': 8,
        '[SEP]': 9
    }
    return InferenceUtil(MAX_SEQ_LEN, TAG2IDX, MODEL, VERSION, SERVER, TIMEOUT)


def get_bert_bilstm_crf_softlexicon_maritime():
    MODEL = 'bert_bilstm_crf_softlexicon_maritime'
    SERVER = 'localhost:8400'
    VERSION = 1
    TIMEOUT = 10
    TAG2IDX = {
        '[PAD]': 0,
        'O': 1,
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
        '[CLS]': 14,
        '[SEP]': 15
    }
    MAX_SEQ_LEN = 32
    return InferenceUtil(MAX_SEQ_LEN, TAG2IDX, MODEL, VERSION, SERVER, TIMEOUT)
