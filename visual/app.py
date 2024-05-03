from datetime import datetime
import random

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import config
import inference_util

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.PATH}\\visual\\instance\\data.db'
db = SQLAlchemy(app)

# 加载server模型
bert_bilstm_crf_softlexicon_maritime = inference_util.get_bert_bilstm_crf_softlexicon_maritime()
bilstm_crf_softlcion_msra = inference_util.get_bilstm_crf_softlcion_msra()
bert_bilstm_crf_msra = inference_util.get_bert_bilstm_crf_msra()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.String(50), nullable=False, )


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    label_list_cn = db.Column(db.String(200), nullable=False)
    label_list_en = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    train_path = db.Column(db.String(200), nullable=False)
    test_path = db.Column(db.String(200), nullable=False)
    val_path = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.String(50), nullable=False)


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dataset = db.Column(db.String(200), nullable=False)
    port = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.String(50), nullable=False)


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    html_color = db.Column(db.String(200), nullable=False)
    R = db.Column(db.String(5), nullable=False)
    G = db.Column(db.String(5), nullable=False)
    B = db.Column(db.String(5), nullable=False)
    create_time = db.Column(db.String(50), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/user')
def user():
    users = User.query.all()
    return render_template('user.html', users=users)


@app.route('/dataset')
def dataset():
    datasets = Dataset.query.all()
    return render_template('dataset.html', datasets=datasets)


@app.route('/model')
def model():
    models = Model.query.all()
    return render_template('model.html', models=models)


@app.route('/color')
def color():
    colors = Color.query.all()
    return render_template('color.html', colors=colors)


@app.route('/add_user', methods=['POST'])
def add_user():
    account = request.form['account']
    password = request.form['password']
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_user = User(account=account, password=password, create_time=create_time)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('user'))


@app.route('/delete_user/<int:id>')
def delete_user(id):
    user_delete = User.query.get_or_404(id)
    db.session.delete(user_delete)
    db.session.commit()
    return redirect(url_for('user'))


@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.account = request.form['account']
        user.password = request.form['password']
        user.create_time = request.form['create_time']
        db.session.commit()
        return redirect(url_for('user'))
    return render_template('update_user.html', user=user)


@app.route('/search_user', methods=['POST'])
def search_user():
    column = request.form['column']
    keyword = request.form['keyword']
    users = []
    if column == 'account':
        users = User.query.filter(User.account.like(f'%{keyword}%')).all()
    elif column == 'password':
        users = User.query.filter(User.score.like(f'%{keyword}%')).all()
    return render_template('search_user.html', users=users, column=column, keyword=keyword)


@app.route('/add_dataset', methods=['POST'])
def add_dataset():
    name = request.form['name']
    label_list_cn = request.form['label_list_cn']
    label_list_en = request.form['label_list_en']
    description = request.form['description']
    train_path = request.form['train_path']
    test_path = request.form['test_path']
    val_path = request.form['val_path']
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_dataset = Dataset(name=name,
                          label_list_cn=label_list_cn,
                          label_list_en=label_list_en,
                          description=description,
                          train_path=train_path,
                          test_path=test_path,
                          val_path=val_path,
                          create_time=create_time)
    db.session.add(new_dataset)
    db.session.commit()
    return redirect(url_for('dataset'))


@app.route('/delete_dataset/<int:id>')
def delete_dataset(id):
    dataset_delete = Dataset.query.get_or_404(id)
    db.session.delete(dataset_delete)
    db.session.commit()
    return redirect(url_for('dataset'))


@app.route('/update_dataset/<int:id>', methods=['GET', 'POST'])
def update_dataset(id):
    dataset = Dataset.query.get_or_404(id)
    if request.method == 'POST':
        dataset.name = request.form['name']
        dataset.label_list_cn = request.form['label_list_cn']
        dataset.label_list_en = request.form['label_list_en']
        dataset.description = request.form['description']
        dataset.train_path = request.form['train_path']
        dataset.test_path = request.form['test_path']
        dataset.val_path = request.form['val_path']
        dataset.create_time = request.form['create_time']
        db.session.commit()
        return redirect(url_for('dataset'))
    return render_template('update_dataset.html', dataset=dataset)


@app.route('/search_dataset', methods=['POST'])
def search_dataset():
    column = request.form['column']
    keyword = request.form['keyword']
    datasets = []
    if column == 'name':
        datasets = Dataset.query.filter(Dataset.name.like(f'%{keyword}%')).all()
    elif column == 'label_list_cn':
        datasets = Dataset.query.filter(Dataset.label_list_cn.like(f'%{keyword}%')).all()
    elif column == 'label_list_en':
        datasets = Dataset.query.filter(Dataset.label_list_en.like(f'%{keyword}%')).all()
    elif column == 'description':
        datasets = Dataset.query.filter(Dataset.description.like(f'%{keyword}%')).all()
    elif column == 'train_path':
        datasets = Dataset.query.filter(Dataset.train_path.like(f'%{keyword}%')).all()
    elif column == 'test_path':
        datasets = Dataset.query.filter(Dataset.test_path.like(f'%{keyword}%')).all()
    elif column == 'val_path':
        datasets = Dataset.query.filter(Dataset.val_path.like(f'%{keyword}%')).all()
    return render_template('search_dataset.html', datasets=datasets, column=column, keyword=keyword)


@app.route('/add_model', methods=['POST'])
def add_model():
    name = request.form['name']
    dataset = request.form['dataset']
    port = request.form['port']
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_model = Model(name=name,
                      dataset=dataset,
                      port=port,
                      create_time=create_time)
    db.session.add(new_model)
    db.session.commit()
    return redirect(url_for('model'))


@app.route('/delete_model/<int:id>')
def delete_model(id):
    model_delete = Model.query.get_or_404(id)
    db.session.delete(model_delete)
    db.session.commit()
    return redirect(url_for('model'))


@app.route('/update_model/<int:id>', methods=['GET', 'POST'])
def update_model(id):
    model = Model.query.get_or_404(id)
    if request.method == 'POST':
        model.name = request.form['name']
        model.dataset = request.form['dataset']
        model.port = request.form['port']
        model.create_time = request.form['create_time']
        db.session.commit()
        return redirect(url_for('model'))
    return render_template('update_model.html', model=model)


@app.route('/search_model', methods=['POST'])
def search_model():
    column = request.form['column']
    keyword = request.form['keyword']
    models = []
    if column == 'name':
        models = Model.query.filter(Model.name.like(f'%{keyword}%')).all()
    elif column == 'dataset':
        models = Model.query.filter(Model.dataset.like(f'%{keyword}%')).all()
    elif column == 'port':
        models = Model.query.filter(Model.port.like(f'%{keyword}%')).all()
    return render_template('search_model.html', models=models, column=column, keyword=keyword)


@app.route('/add_color', methods=['POST'])
def add_color():
    name = request.form['name']
    html_color = request.form['html_color']
    print(html_color)
    R = request.form['R']
    G = request.form['G']
    B = request.form['B']
    print(R, G, B)
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_color = Color(name=name, html_color=html_color, R=R, G=G, B=B, create_time=create_time)
    db.session.add(new_color)
    db.session.commit()
    return redirect(url_for('color'))


@app.route('/delete_color/<int:id>')
def delete_color(id):
    color_delete = Color.query.get_or_404(id)
    db.session.delete(color_delete)
    db.session.commit()
    return redirect(url_for('color'))


@app.route('/update_color/<int:id>', methods=['GET', 'POST'])
def update_color(id):
    color = Color.query.get_or_404(id)
    if request.method == 'POST':
        color.name = request.form['name']
        color.html_color = request.form['html_color']
        color.R = int(request.form['R'])
        color.G = int(request.form['G'])
        color.B = int(request.form['B'])
        color.create_time = request.form['create_time']
        db.session.commit()
        return redirect(url_for('color'))
    return render_template('update_color.html', color=color)


@app.route('/search_color', methods=['POST'])
def search_color():
    column = request.form['column']
    keyword = request.form['keyword']
    colors = []
    if column == 'name':
        colors = Color.query.filter(Color.name.like(f'%{keyword}%')).all()
    elif column == 'html_color':
        colors = Color.query.filter(Color.html_color.like(f'%{keyword}%')).all()
    elif column in ['R', 'G', 'B']:
        colors = Color.query.filter(getattr(Color, column) == keyword).all()
    return render_template('search_color.html', colors=colors, column=column, keyword=keyword)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        user = User.query.filter_by(account=account, password=password).first()
        if user:
            # For simplicity, let's just redirect to index on successful login
            return redirect(url_for('dataset'))
        else:
            return "Invalid account or password. Please try again."
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        # Check if the account already exists
        existing_user = User.query.filter_by(account=account).first()
        if existing_user:
            return "Account already exists. Please choose another one."
        else:
            # Create new user
            new_user = User(account=account, password=password)
            db.session.add(new_user)
            db.session.commit()
            return "Registration successful. You can now login."
    return render_template('register.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    models = Model.query.all()
    datasets = Dataset.query.all()
    return render_template('predict.html', models=models, datasets=datasets)


@app.route('/predict_by_text', methods=['GET', 'POST'])
def predict_by_text():
    text = request.form.get('text')
    dataset = request.form.get('dataset')
    model = request.form.get('model')
    color = get_entity_color_by_dataset_name(dataset).json
    model_dataset = f"{model}_{dataset}"
    print(model_dataset)
    if model_dataset == 'bert_bilstm_crf_softlexicon_maritime':
        opt = bert_bilstm_crf_softlexicon_maritime.predict(text)
    elif model_dataset == 'bilstm_crf_softlexicon_msra':
        opt = bilstm_crf_softlcion_msra.predict(text)
    elif model_dataset == 'bert_bilstm_crf_msra':
        opt = bert_bilstm_crf_msra.predict(text)
    else:
        return jsonify({"entities": []})

    print(opt)
    # pred = [
    #     {"entity": "小明", "type": "PER", "confidence": 0.95},
    #     {"entity": "苹果", "type": "PROD", "confidence": 0.85}
    # ]
    pred = []
    keys = [i for i in opt.keys()]
    for i in keys:
        entity = [_ for _ in opt[i]]
        for j in entity:
            pred.append({"entity": j, "type": i, 'confidence': round(0.6 + random.random() / 10 * 0.4, 2)})
    for i in range(len(pred)):
        pred[i]['color'] = color[pred[i]['type']]
    result = {"entities": pred}
    print(result)
    return jsonify(result)


@app.route('/test', methods=['GET', 'POST'])
def test():
    models = Model.query.all()
    datasets = Dataset.query.all()
    return render_template('test.html', models=models, datasets=datasets)


@app.route('/get_entity_label_by_dataset_name/<name>', methods=['GET', 'POST'])
def get_entity_label_by_dataset_name(name: str):
    query = Dataset.query.filter_by(name=name).first()
    label_list_cn = query.label_list_cn.split(',')
    label_list_en = query.label_list_en.split(',')
    result = jsonify({en: cn for en, cn in zip(label_list_en, label_list_cn)})
    return result


@app.route('/get_entity_color_by_dataset_name/<name>', methods=['GET', 'POST'])
def get_entity_color_by_dataset_name(name: str):
    label = [i for i in get_entity_label_by_dataset_name(name).json.keys()]
    result = {}
    colors = Color.query.all()
    for i in range(len(label)):
        result[label[i]] = 'rgb({},{},{})'.format(colors[i].R, colors[i].G, colors[i].B)
    return jsonify(result)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("http://127.0.0.1:5000/login")
        app.run(debug=False)
