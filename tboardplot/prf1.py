import os

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker

import config

model_name = 'Bert-BiLstm-CRF-Softlexicon'

path = config.PATH + '/tboardplot/data/'

data = os.listdir(path)

p = pd.read_csv(path + [i for i in data if 'precision' in i][0])["Value"]
r = pd.read_csv(path + [i for i in data if 'recall' in i][0])["Value"]
f1 = pd.read_csv(path + [i for i in data if 'f1' in i][0])["Value"]
acc = pd.read_csv(path + [i for i in data if 'accuracy' in i][0])["Value"]

step = pd.read_csv(path + [i for i in data if 'precision' in i][0])["Step"]

plt.plot(step, p, label="$Precision$", color="lightgreen")
plt.plot(step, r, label="$Recall$", color="lightpink")
plt.plot(step, f1, label="$f_1$", color="lightblue")
plt.plot(step, acc, label="$Accuracy$", color="green")
plt.legend()
plt.xlabel("step")
plt.ylabel("value")
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
plt.title(model_name + "'s Metrics")
plt.show()
