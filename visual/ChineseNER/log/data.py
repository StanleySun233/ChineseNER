import re
import pandas as pd
import matplotlib.pyplot as plt

f = open("train.log", "r").read()

s = '2024-04-09 11:33:32,513 - log/train.log - INFO - accuracy:  87.94%; precision:  71.41%; recall:  66.42%; FB1:  68.83'
dt = re.findall(r'accuracy:(.*?)%; precision:(.*?)%; recall:(.*?)%; FB1:(.*?)\n', f)

for i in range(len(dt)):
    dt[i] = [float(j.replace(" ", '')) for j in dt[i]]

dt = pd.DataFrame(dt, columns=['accuracy', 'precision', 'recall', 'FB1'])
dt.to_csv('test.csv', encoding='utf-8', index=False)

# plt.plot(range(len(dt['accuracy'])), dt['accuracy'], label='precision')
plt.plot(range(len(dt['precision'])), dt['precision'], label='precision')
plt.plot(range(len(dt['recall'])), dt['recall'], label='recall')
plt.plot(range(len(dt['FB1'])), dt['FB1'], label='F1')
plt.legend(loc='best')
plt.xlabel("epoch")
plt.ylabel("%")
plt.show()
