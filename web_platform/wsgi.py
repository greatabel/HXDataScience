"""App entry point."""
import os
import json

import flask_login
from flask import request
from flask import url_for
from flask import redirect
from flask import Blueprint, render_template as rt

from flask import Flask, Response

from movie import create_app
from movie.domain.model import Director, User, Review, Movie


app = create_app()
app.secret_key = "ABCabc123"
app.debug = True


login_manager = flask_login.LoginManager(app)
user_pass = {}

@app.route("/statistics", methods=['GET'])
def relationship():
    # static/data/test_data.json
    filename = os.path.join(app.static_folder, 'data.json')
    with open(filename) as test_file:
        d = json.load(test_file)
    print(type(d), '#'*10, d)
    return d

@login_manager.user_loader
def load_user(email):
    return user_pass.get(email, None)


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = user_pass.get(email, None)
    if stored_user and password == stored_user.password:

        flask_login.login_user(stored_user)
        print(stored_user.is_active, 'login')
        return redirect(url_for('review'))
    else:
        print('login fail')
    return redirect(url_for('home_bp.home',pagenum=1))


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for('home_bp.home',pagenum=1))
    # if DB.get_user(email):
    if email in user_pass:
        print('already existed user')
        return redirect(url_for('home_bp.home',pagenum=1))
    # salt = PH.get_salt()
    # hashed = PH.get_hash(pw1 + salt)
    print('register', email, pw1)
    user = User(email, pw1)
    user_pass[email] = user
    print('register', user_pass, '#'*5)
    return redirect(url_for('home_bp.home',pagenum=1))


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for('home_bp.home',pagenum=1))

reviews = []
@app.route("/review", methods=["GET", "POST"])
@flask_login.login_required
def review():
    if request.method == "POST":
        
        movie_name = request.form['movie_name']
        movie_id = request.form['movie_id']
        rtext = request.form['rtext']
        rating = request.form['rating']

        movie = Movie(movie_name, 1990, int(movie_id))
        review = Review(movie, rtext, int(rating))
        reviews.append(review)


    return rt(
        'review.html',
        reviews=reviews,
        
    )



@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

# --------------------------

@app.route('/', methods=['GET'])
def index():
    return rt('./index.html')


@app.route('/file/upload', methods=['POST'])
def upload_part():  # 接收前端上传的一个分片
    task = request.form.get('task_id')  # 获取文件的唯一标识符
    chunk = request.form.get('chunk', 0)  # 获取该分片在所有分片中的序号
    filename = '%s%s' % (task, chunk)  # 构造该分片的唯一标识符

    upload_file = request.files['file']
    upload_file.save('./upload/%s' % filename)  # 保存分片到本地
    return rt('./index.html')


@app.route('/file/merge', methods=['GET'])
def upload_success():  # 按序读出分片内容，并写入新文件
    target_filename = request.args.get('filename')  # 获取上传文件的文件名
    task = request.args.get('task_id')  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    with open('./upload/%s' % target_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间

    return rt('./index.html')


@app.route('/file/list', methods=['GET'])
def file_list():
    files = os.listdir('./upload/')  # 获取文件目录
    # print(type(files))
    files.remove('.DS_Store')
    # files = map(lambda x: x if isinstance(x, unicode) else x.decode('utf-8'), files)  # 注意编码
    return rt('./list.html', files=files)


@app.route('/file/download/<filename>', methods=['GET'])
def file_download(filename):
    def send_chunk():  # 流式读取
        store_path = './upload/%s' % filename
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')

# --------------------------

if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False)

