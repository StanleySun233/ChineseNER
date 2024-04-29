from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# 模拟的命名实体识别函数
def predict_named_entities(text):
    # 这里可以替换为您的真实模型推理过程
    entities = [
        {"entity": "小明", "type": "PER", "confidence": 0.95},
        {"entity": "苹果", "type": "PROD", "confidence": 0.85}
    ]
    return entities


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        text = request.form['text']
        entities = predict_named_entities(text)
        return jsonify(entities)


if __name__ == '__main__':
    app.run(debug=True)
