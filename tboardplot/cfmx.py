import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import config

PATH = config.PATH + "/tboardplot/cfmx/"
TAG_FILE = 'maritime_bert_bilstm_crf_softlexicon_tag_predict.csv'
LABEL = config.MARITIME


def confusion_matrix_tag_from_csv(path, labels):
    # 从CSV文件加载数据
    df = pd.read_csv(path)
    df = df[df["y_true"] != 1]

    # 获取y_true和y_pred列的值
    y_true = df['y_true']
    y_pred = df['y_pred']

    # 创建混淆矩阵
    cm = confusion_matrix(y_true, y_pred)

    # 使用Seaborn绘制混淆矩阵
    plt.figure(figsize=(len(labels), len(labels)))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()


confusion_matrix_tag_from_csv(PATH + TAG_FILE, ['O'] + [i for i in LABEL.keys()])