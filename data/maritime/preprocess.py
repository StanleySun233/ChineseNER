# -*-coding:utf-8 -*-
import config
from data.base_preprocess import get_instance, read_text
from data.word_enhance import WordEnhanceMethod
from data.tokenizer import Tokenizers

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

MAPPING = {
    'train': 'train',
    'dev': 'valid',
    'test': 'predict'
}


def load_data(data_dir, file_name):
    """
    Load line and generate sentence and tag list with char split by ' '
    sentences: ['今 天 天 气 好 ', ]
    tags: ['O O O O O ', ]
    """
    tokens = read_text(data_dir, 'example.{}'.format(file_name))
    sentences = []
    tags = []
    tag = []
    sentence = []
    for i in tokens:
        if i == '':
            # Here join by ' ' to avoid bert_tokenizer merging tokens
            sentences.append(' '.join(sentence))
            tags.append(' '.join(tag))
            tag = []
            sentence = []
        else:
            s, t = i.split(' ')
            tag.append(t)
            sentence.append(s)
    return sentences, tags


if __name__ == '__main__':
    data_dir = config.PATH + "/data/maritime"

    for tokenizer in Tokenizers:
        for word_enhance in [None] + WordEnhanceMethod:
            for file in MAPPING:
                print('Dumping TF Record for {} word_enhance = {} tokenizer = {}'. \
                      format(file, word_enhance, tokenizer))
                prep = get_instance(tokenizer, MAX_SEQ_LEN, TAG2IDX, MAPPING, word_enhance)
                prep.init_data(data_dir, file, load_data)
                prep.dump_tfrecord()
