1. RUN

```shell
python main.py --model bert_bilstm_crf_softlexicon --data maritime
tensorboard --logdir ./checkpoint/ner_maritime_bert_bilstm_crf_softlexicon
```

2. EVAL

```shell 
## 单模型：输出tag级别和entity级别详细结果
python evaluation.py --model bert_bilstm_crf --data msra
python evaluation.py --model bert_bilstm_crf_mtl_msra_msr --data msra ##注意多任务model_name=model_name_{task1}_{task2}
```

3. INFERENCE

```shell
docker run -it --rm -p 8500:8500 -v "D:/data/ChineseNER/serving_model/bilstm_crf_softlexicon_msra:/models/bilstm_crf_softlexicon_msra" -e MODEL_NAME=bilstm_crf_softlexicon_msra tensorflow/serving:1.15.0-gpu

docker run -it --rm -p 8400:8500 -v "D:/data/ChineseNER/serving_model/bert_bilstm_crf_softlexicon_maritime:/models/bert_bilstm_crf_softlexicon_maritime" -e MODEL_NAME=bert_bilstm_crf_softlexicon_maritime tensorflow/serving:1.15.0-gpu
```