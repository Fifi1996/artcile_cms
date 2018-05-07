# 使用sqlalchemy防止数据迁移更换数据库
# coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/artcms"
app.config["SQLALCHEMY_ON_TEARDOWN"] = True

db = SQLAlchemy(app)


# 用户表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(20), nullable=False)  # 账号
    pwd = db.Column(db.String(100), nullable=False)  # 密码
    addtime = db.Column(db.DateTime, nullable=False)  # 添加注册时间

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)


# 文章表
class Art(db.Model):
    __tablename__ = "art"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(100), nullable=False)  # 标题
    cate = db.Column(db.Integer, nullable=False)  # 分类
    user_id = db.Column(db.Integer, nullable=False)  # 作者
    logo = db.Column(db.Integer, nullable=False)  # 封面
    content = db.Column(db.Text, nullable=False)
    addtime = db.Column(db.DateTime, nullable=False)  # 添加注册时间

    def __repr__(self):
        return "<Art %r>" % self.title


if __name__ == "__main__":
    db.create_all()
