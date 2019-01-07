from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, TextAreaField, FileField
from app.models import User
from app.settings import icon_allow_mode
from flask import session


class RegisterForm(FlaskForm):
    def validata_name(self, field):
        name = field.data
        user = User.query.filter_by(username=name).count()
        if user == 1:
            raise ValidationError("昵称已存在！")

    def validata_email(self, field):
        email = field.data
        email = User.query.filter_by(email=email).count()
        if email == 1:
            raise ValidationError("邮箱已存在！")

    def validata_phone(self, field):
        telephone = field.data
        phone = User.query.filter_by(telephone=telephone).count()
        if phone == 1:
            raise ValidationError("号码已存在！")

    username = StringField(
        "用户名",
        [
            validators.DataRequired("昵称不能为空！"),
            validators.Length(min=2, max=8, message="昵称长度在3至8之间！"),
            validata_name,
        ],
        description="用户名",
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "昵称",
            "autofocus": "",
        },
    )
    email = StringField(
        "邮箱",
        [
            validators.DataRequired("邮箱不能为空！"),
            validators.Email("邮箱格式不正确！"),
            validata_email,
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "邮箱",
            "autofocus": "",
        },
    )
    telephone = StringField(
        "手机号码",
        [
            validators.DataRequired("手机号码不能为空！"),
            validators.Regexp("1[3578]\\d{9}", message=" 手机号码格式不正确！"),
            validata_phone,
        ],
        description="手机号码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "手机",
            'type': 'number',
            "autofocus": "",
        },
    )
    password = PasswordField(
        "密码",
        [
            validators.DataRequired("密码不能为空！"),
            validators.Length(min=5, max=20, message="密码长度在5至20之间！")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "密码",
            "autofocus": "",
        },
    )
    re_password = PasswordField(
        "确认密码",
        [
            validators.DataRequired("密码不能为空！"),
            validators.Length(min=5, max=20, message="密码长度在5至20之间！"),
            validators.EqualTo("password", message="两次输入密码不一致！"),
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "密码",
            "autofocus": "",
        },
    )
    submit = SubmitField(
        "立即注册",
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )


class LoginForm(FlaskForm):
    username = StringField(
        "账号",
        [
            validators.DataRequired("请输入账号！"),
            validators.Length(max=20, message="不能低于5位！")
        ],
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "用户名/邮箱/手机号码",
            "autofocus": "",
        },
    )
    password = PasswordField(
        "密码",
        [
            validators.DataRequired("请输入密码！"),
            validators.Length(min=5, max=20, message="密码长度应在5位以上！"),
        ],
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "密码",
        },
    )
    submit = SubmitField(
        "立即登录",
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        },
    )


class UserForm(FlaskForm):
    def validata_name(self, field):
        name = field.data
        raw_username = User.query.filter_by(id=session["userid"]).first().username
        if raw_username != name:
            user = User.query.filter_by(username=name).count()
            if user == 1:
                raise ValidationError("昵称已存在！")

    def validata_email(self, field):
        email = field.data
        raw_email = User.query.filter_by(id=session["userid"]).first().email
        if raw_email != email:
            email = User.query.filter_by(email=email).count()
            if email == 1:
                raise ValidationError("邮箱已存在！")

    def validata_phone(self, field):
        telephone = field.data
        raw_telephone = User.query.filter_by(id=session["userid"]).first().telephone
        if raw_telephone != telephone:
            phone = User.query.filter_by(telephone=telephone).count()
            if phone == 1:
                raise ValidationError("号码已存在！")

    def validata_icon(self, field):
        if type(field.data) != str:
            icon = field.data.filename
            if not icon.split(".")[-1] in icon_allow_mode:
                raise ValidationError("图片格式不允许！")

    username = StringField(
        "昵称",
        [
            validators.DataRequired("请输入账号！"),
            validators.Length(min=3, max=20, message="不能低于5位！"),
            validata_name,
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "昵称",
            "autofocus": "",
        },
    )
    email = StringField(
        "邮箱",
        [
            validators.DataRequired("邮箱不能为空！"),
            validators.Email("邮箱格式不正确！"),
            validata_email,
        ],
        description="邮箱",
        render_kw={
            "class": "form-control",
            "placeholder": "邮箱",
            "autofocus": "",
        },
    )
    telephone = StringField(
        "手机号码",
        [
            validators.DataRequired("手机号码不能为空！"),
            validators.Regexp("1[3578]\\d{9}", message=" 手机号码格式不正确！"),
            validata_phone,
        ],
        description="手机号码",
        render_kw={
            "class": "form-control",
            "placeholder": "手机",
            "autofocus": "",
        },
    )
    icon = FileField(
        "头像上传",
        [validata_icon],
        render_kw={
            "id": "input_face",
            "class": "form-control",
            "style": "display:none",
            "autofocus": "",
        }
    )
    info = StringField(
        "个性简介",
        [
        ],
        description="个性简介",
        render_kw={
            "class": "form-control",
            "placeholder": "个人简介",
            # "rows": "4",
        },
    )
    submit = SubmitField(
        "保存修改",
        render_kw={
            "id": "user_submit",
            "style": "display:none",
        },
    )


class PasswordForm(FlaskForm):
    password = PasswordField(
        "旧密码",
        [validators.DataRequired("请输入密码！"),
         validators.Length(min=5, max=20, message="密码长度应在5位以上！")
         ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "旧密码",
            "autofocus": "",
        }
    )
    new_password = PasswordField(
        "新密码",
        [validators.DataRequired("请输入密码！"),
         validators.Length(min=5, max=20, message="密码长度应在5位以上！")
         ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "新密码",
            "autofocus": "",
        }
    )
    submit = SubmitField(
        "修改密码",
        render_kw={
            "id": "user_submit",
            "style": "display:none",
        },
    )


