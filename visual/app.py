from flask import Flask, render_template, request, jsonify
import os
from ChineseNER.main import evaluate_input

app = Flask(__name__)


# 模拟的命名实体识别函数
def predict_named_entities(text):
    # 这里可以替换为您的真实模型推理过程
    raw = evaluate_input(text)["entities"]
    entities = [{"entity": i["word"],
                 "type": i["type"],
                 "confidence": 0.99} for i in raw]
    print(entities)
    return entities


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        text = request.form['text']
        entities = predict_named_entities(text)
        return jsonify(entities)


if __name__ == '__main__':
    app.run(debug=True)
