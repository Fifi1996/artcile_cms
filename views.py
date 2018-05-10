# coding: utf-8
import sys
import importlib

importlib.reload(sys)
from flask import Flask, render_template, redirect, flash, session, Response, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, ArtForm, ArtEditForm
from models import User, db, Art
from werkzeug.security import generate_password_hash
import datetime
import os
import pymysql
from werkzeug.utils import secure_filename
from functools import wraps
import uuid

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"
app.config["UP"] = os.path.join(os.path.dirname(__file__), "static/uploads")


# 登录装饰器,权限控制
def user_login_req(f):
    @wraps(f)
    def login_req(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return login_req


# 登录
@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        session["user"] = data["name"]
        flash("登录成功", "ok")
        return redirect("/art/list/1/")
    return render_template("login.html", title="登录", form=form)  # 渲染模版


# 用户注册
@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # 验证注册数据
        data = form.data
        # 保存数据
        user = User(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            addtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(user)
        db.session.commit()
        # 定义会话闪现
        flash("注册成功，请登录！", "ok")
        return redirect("/login/")
    else:
        flash("请输入正确信息", "err")

    return render_template("register.html", title="注册", form=form)


# 用户退出（跳转到登录页面302重定向）
@app.route("/logout/", methods=["GET"])
@user_login_req
def logout():
    session.pop("user", None)
    return redirect("/login/")


# 修改文件名称
def change_name(name):
    info = os.path.splitext(name)
    # 文件名：时间格式字符+唯一字符串+后缀名
    name = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + info[-1]
    return name


# 发布文章
@app.route("/art/add/", methods=["GET", "POST"])
@user_login_req
def art_add():
    form = ArtForm()
    if form.validate_on_submit():
        data = form.data
        # 上传logo
        file = secure_filename(form.logo.data.filename)
        logo = change_name(file)
        if not os.path.exists(app.config["UP"]):
            os.mkdir(app.config["UP"])
        # 保存文件
        form.logo.data.save(app.config["UP"] + "/" + logo)
        # 获取用户id
        user = User.query.filter_by(name=session["user"]).first()
        user_id = user.id
        # 保存数据
        art = Art(
            title=data["title"],
            cate=data["cate"],
            user_id=user_id,
            logo=logo,
            content=data["content"],
            addtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(art)
        db.session.commit()
        flash("发布文章成功", "ok")
    return render_template("art_add.html", title="发布文章", form=form)


# 编辑文章
@app.route("/art/edit/<int:id>/", methods=["GET", "POST"])
@user_login_req
def art_edit(id):  # 指定id
    art = Art.query.get_or_404(int(id))
    form = ArtEditForm()
    if request.method == "GET":
        form.content.data = art.content
        form.cate.data = art.cate
        form.logo.data = art.logo
    if form.validate_on_submit():
        data = form.data
        # 上传logo
        file = secure_filename(form.logo.data.filename)
        logo = change_name(file)
        if not os.path.exists(app.config["UP"]):
            os.makedirs(app.config["UP"])
        # 保存文件
        form.logo.data.save(app.config["UP"] + "/" + logo)
        art.logo = logo
        art.title = data["title"]
        art.content = data["content"]
        art.cate = data["cate"]
        db.session.add(art)
        db.session.commit()
        flash("文章编辑成功", "ok")

    return render_template("art_edit.html", form=form, title="编辑文章", art=art)


# 删除文章
@app.route("/art/del/<int:id>/", methods=["GET"])
# @user_login_req
def art_del(id):
    art = Art.query.get_or_404(int(id))
    db.session.delete(art)
    db.session.commit()
    flash("删除《%s》成功" % art.title, "ok")
    return redirect("/art/list/1/")


# 文章列表
@app.route("/art/list/<int:page>/", methods=["GET"])
# @user_login_req
def art_list(page=None):
    if page is None:
        page = 1
    user = User.query.filter_by(name=session["user"]).first()
    page_data = Art.query.filter_by(
        user_id=user.id
    ).order_by(
        Art.addtime.desc()
    ).paginate(page=page, per_page=1)
    cate = [(1, "python"), (2, "test"), (3, "android")]
    return render_template("art_list.html", title="文章列表", page_data=page_data, cate=cate)


# 验证码
@app.route("/codes/", methods=["GET"])
def codes():
    from codes import Codes
    c = Codes()
    info = c.create_code()
    image = os.path.join(os.path.dirname(__file__), "static/code") + "/" + info["img_name"]
    with open(image, 'rb') as f:
        image = f.read()
    session["code"] = info["code"]
    # print(session["code"])
    return Response(image, mimetype="ipeg")


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)
