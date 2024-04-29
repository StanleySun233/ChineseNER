import inference_util

model = inference_util.get_bert_bilstm_crf_softlexicon_maritime()

while True:
    print(model.predict(input("Text:")))
    # 小孙今年二十一岁，在上海海事大学担任学生职务。
