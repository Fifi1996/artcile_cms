# coding:utf8
# 登录表单：账户 密码 登录按钮
# 注册：账户 密码 确认密码 验证码 注册按钮
# 发布文章：标题 分类 封面 内容 发布文章按钮
from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import User


class LoginForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("账户不能为空")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号："
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码："
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_pwd(self, field):
        pwd = field.data
        user = User.query.filter_by(name=self.name.data).first
        if not user.check_pwd(pwd):
            raise ValidationError("密码错误！")


class RegisterForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("账号不能为空！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号："
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码："
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("确认密码不能为空！"),
            EqualTo('pwd', message="两次密码不一致!")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入确认密码："
        }
    )
    code = StringField(
        label="验证码",
        validators=[
            DataRequired("验证码不能为空！")
        ],
        description="验证码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入验证码："
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class": "btn btn-success"
        }
    )

    # 自定义字段验证规则
    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user > 0:
            raise ValidationError("账号已存在，不能重复注册")

    # 自定义验证码验证功能
    def validate_code(self, field):
        code = field.data
        if not session.keys("code"):
            raise ValidationError("没有验证码！")
        if session.keys("code") and session["code"].lower() != code.lower():
            raise ValidationError("验证码错误!")

#发布文章
class ArtForm(FlaskForm):
    title = StringField(
        label="标题",
        validators=[
            DataRequired("标题不能为空")
        ],
        description="验证码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入标题;"
        }
    )
    cate = SelectField(
        label="分类",
        validators=[
            DataRequired("分类不能为空")
        ],
        description="分类",
        choices=[(1, "python"), (2, "test"), (3, "android")],
        default=1,
        coerce=int,
        render_kw={
            "class": "form-control"
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("封面不能为空")
        ],
        description="封面",
        render_kw={
            "class": "form-control-file"
        }
    )
    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired("内容不能为空")
        ],
        description="内容",
        render_kw={
            "style": "height:300px:",
            "id": "content"
        }
    )
    submit = SubmitField(
        "发布文章",
        render_kw={
            "class": "btn btn-primary"
        }
    )
