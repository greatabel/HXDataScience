"""App entry point."""
import os
import sys
import json

import flask_login
from flask import request
from flask import url_for
from flask import redirect, session
from flask import Blueprint, render_template as rt
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, Response
from flask import jsonify

from movie import create_app
from movie.domain.model import Director, Review, Movie
import i0bash_caller

try:
    print(sys.version)
    import pydoop.hdfs as hdfs
except ImportError as error:
    # Output expected ImportErrors.
    print(error)


app = create_app()
app.secret_key = "ABCabc123"
app.debug = True

# ---start  数据库 ---

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hx_data.db"
db = SQLAlchemy(app)

# --- end   数据库 ---


class User(db.Model):
    """ Create user table"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password


login_manager = flask_login.LoginManager(app)
user_pass = {}

@app.route("/call_bash", methods=["GET"])
def call_bash():
    i0bash_caller.open_client("")
    return {}, 200
    

@app.route("/statistics", methods=["GET"])
def relationship():
    # static/data/test_data.json
    filename = os.path.join(app.static_folder, "data.json")
    with open(filename) as test_file:
        d = json.load(test_file)
    print(type(d), "#" * 10, d)
    return d


@login_manager.user_loader
def load_user(email):
    return user_pass.get(email, None)


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        data = User.query.filter_by(username=email, password=password).first()
        print(data, "@" * 10)
        if data is not None:
            print("test login")
            session["logged_in"] = True
            print("login sucess", "#" * 20)
            return redirect(url_for("home_bp.home", pagenum=1))
        else:
            return "Not Login"
    except:
        return "Not Login"
    return redirect(url_for("home_bp.home", pagenum=1))


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for("home_bp.home", pagenum=1))
    # if DB.get_user(email):
    if email in user_pass:
        print("already existed user")
        return redirect(url_for("home_bp.home", pagenum=1))
    # salt = PH.get_salt()
    # hashed = PH.get_hash(pw1 + salt)
    print("register", email, pw1)
    new_user = User(username=email, password=pw1)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("home_bp.home", pagenum=1))


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("home_bp.home", pagenum=1))


reviews = []


@app.route("/review", methods=["GET", "POST"])
@flask_login.login_required
def review():
    if request.method == "POST":

        movie_name = request.form["movie_name"]
        movie_id = request.form["movie_id"]
        rtext = request.form["rtext"]
        rating = request.form["rating"]

        movie = Movie(movie_name, 1990, int(movie_id))
        review = Review(movie, rtext, int(rating))
        reviews.append(review)

    return rt(
        "review.html",
        reviews=reviews,
    )


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized"


# --------------------------


@app.route("/", methods=["GET"])
def index():
    return rt("./index.html")


@app.route("/file/upload", methods=["POST"])
def upload_part():  # 接收前端上传的一个分片
    task = request.form.get("task_id")  # 获取文件的唯一标识符
    chunk = request.form.get("chunk", 0)  # 获取该分片在所有分片中的序号
    filename = "%s%s" % (task, chunk)  # 构造该分片的唯一标识符

    upload_file = request.files["file"]
    upload_file.save("./upload/%s" % filename)  # 保存分片到本地
    return rt("./index.html")


@app.route("/file/merge", methods=["GET"])
def upload_success():  # 按序读出分片内容，并写入新文件
    target_filename = request.args.get("filename")  # 获取上传文件的文件名
    task = request.args.get("task_id")  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    with open("./upload/%s" % target_filename, "wb") as target_file:  # 创建新文件
        while True:
            try:
                filename = "./upload/%s%d" % (task, chunk)
                source_file = open(filename, "rb")  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间

    return rt("./index.html")


@app.route("/file/list", methods=["GET"])
def file_list():
    files = os.listdir("./upload/")  # 获取文件目录
    # print(type(files))
    files.remove(".DS_Store")
    # files = map(lambda x: x if isinstance(x, unicode) else x.decode('utf-8'), files)  # 注意编码
    return rt("./list.html", files=files)


@app.route("/file/download/<filename>", methods=["GET"])
def file_download(filename):
    def send_chunk():  # 流式读取
        store_path = "./upload/%s" % filename
        with open(store_path, "rb") as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type="application/octet-stream")


# --------------------------


@app.route("/senordata", methods=["GET"])
def senordata():

    searchdate = request.args.get("searchdate")
    print(searchdate, "in /senordata")
    if searchdate is None:
        return 405, "not allowed"

    print("---get from hdfs ---")
    lines = []
    with hdfs.open("hdfs://127.0.0.1:9000/data/source_demo.csv") as f:
        for line in f:
            # print(line, type(line))
            l = line.decode("utf-8")
            if "2020-11-15" in l:
                lines.append(l)
    print(lines)
    print("---end get from hdfs----")

    # compatible for data post from url for putao and
    # data post from body for try-out approval from Apple
    # in future, front end unify send method, it need to amodify
    result = {}

    result["data"] = lines
    return jsonify(result)


if __name__ == "__main__":
    db.create_all()
    app.run(host="localhost", port=5000, threaded=False)
