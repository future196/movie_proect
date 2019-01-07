from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, validators, FileField, TextAreaField, \
    SelectField, IntegerField, ValidationError, RadioField, BooleanField, SelectMultipleField
from app.settings import picture_allow_mode, movie_allow_mode
from app.models import Movie, Preview, Auth, Role, Admin


class LoginForm(FlaskForm):
    account = StringField(
        "账号",
        [validators.DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "账号",
            "maxlength": "20",
        },
    )
    password = PasswordField(
        "密码",
        [validators.DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "密码",
            "maxlength": "20",
        },
    )
    submit = SubmitField(
        "立即登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
        ,
    )


class TagAddForm(FlaskForm):
    tag = StringField(
        "标签",
        [validators.DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入标签名称",
            "minlength": "2",
            "maxlength": "5",
        },
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary",
        },
    )


class EditTagForm(FlaskForm):
    tag = StringField(
        "标签",
        [validators.DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入标签名称",
            "minlength": "2",
            "maxlength": "5",
        },
    )
    submit = SubmitField(
        "修改",
        render_kw={
            "class": "btn btn-primary",
        },
    )


class MovieForm(FlaskForm):
    def validata_name(self, field):
        name = field.data
        if Movie.query.filter_by(name=name).count() == 1:
            raise ValidationError("片名已重复！")

    def validata_logo(self, field):
        if type(field.data) != str:
            icon = field.data.filename
            if not icon.split(".")[-1] in picture_allow_mode:
                raise ValidationError("图片格式不允许！")

    def validata_movie(self, field):
        if type(field.data) != str:
            icon = field.data.filename
            if not icon.split(".")[-1] in movie_allow_mode:
                raise ValidationError("视频格式不允许！")

    name = StringField(
        "片名",
        [
            validators.DataRequired("不可为空！"),
            validata_name
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片名",
            "maxlength": "20",
        },
    )
    movie = FileField(
        "文件",
        [
            validators.DataRequired("不可为空！"),
            validata_movie,
        ],
        render_kw={
        },
    )
    content = TextAreaField(
        "介绍",
        [validators.DataRequired("不可为空！")],
        render_kw={
            "class": "form-control",
            "rows": "10",
            "maxlength": "200",
        }
    )
    logo = FileField(
        "封面",
        [
            validators.DataRequired("不可为空！"),
            validata_logo,
        ],
        render_kw={
        },
    )

    star = SelectField(
        "星级",
        [validators.DataRequired("请选择！")],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        render_kw={
            "class": "form-control",
        },
    )

    tag = SelectField(
        "标签",
        [validators.DataRequired("请选择！")],
        coerce=int,
        choices=[],
        render_kw={
            "class": "form-control",
        },
    )
    area = StringField(
        "地区",
        [validators.DataRequired("不可为空！")],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区",
            "maxlength": "10",
        },
    )
    length = IntegerField(
        "时长，单位：秒",
        [validators.DataRequired("不可为空！")],
        render_kw={
            "class": "form-control",
            "placeholder": "单位：秒",
            "type": "number",
        },
    )
    release_time = StringField(
        "上映时间",
        [validators.DataRequired("请选择！")],
        render_kw={
            "class": "form-control",
            "type": "date",
        },
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary",
        },
    )


class EditMovieForm(FlaskForm):
    def validata_logo(self, field):
        if type(field.data) != str:
            icon = field.data.filename
            if not icon.split(".")[-1] in picture_allow_mode:
                raise ValidationError("图片格式不允许！")

    def validata_movie(self, field):
        if type(field.data) != str:
            icon = field.data.filename
            if not icon.split(".")[-1] in movie_allow_mode:
                raise ValidationError("视频格式不允许！")

    name = StringField(
        "片名",
        [
            validators.DataRequired("不可为空！"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片名",
            "maxlength": "20",
        },
    )
    movie = FileField(
        "文件",
        [
            validata_movie,
        ],
        render_kw={
        },
    )
    content = TextAreaField(
        "介绍",
        [validators.DataRequired("不可为空！")],
        render_kw={
            "class": "form-control",
            "rows": "10",
            "maxlength": "200",
        }
    )
    logo = FileField(
        "封面",
        [
            validata_logo,
        ],
        render_kw={
        },
    )

    star = SelectField(
        "星级",
        [validators.DataRequired("请选择！")],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        render_kw={
            "class": "form-control",
        },
    )

    tag = SelectField(
        "标签",
        [validators.DataRequired("请选择！")],
        coerce=int,
        choices=[],
        render_kw={
            "class": "form-control",
        },
    )
    area = StringField(
        "地区",
        [validators.DataRequired("不可为空！")],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区",
            "maxlength": "10",
        },
    )
    length = IntegerField(
        "时长，单位：秒",
        [validators.DataRequired("不可为空！")],
        render_kw={
            "class": "form-control",
            "placeholder": "单位：秒",
            "type": "number",
        },
    )
    release_time = StringField(
        "上映时间",
        [validators.DataRequired("请选择！")],
        render_kw={
            "class": "form-control",
            "type": "date",
        },
    )
    submit = SubmitField(
        "修改",
        render_kw={
            "class": "btn btn-primary",
        },
    )


class PreviewForm(FlaskForm):
    def validata_name(self, field):
        name = field.data
        if Preview.query.filter_by(name=name).count() == 1:
            raise ValidationError("预告标题已重复！")

    def validata_logo(self, field):
        if type(field.data) != str:
            icon = field.data.filename
            if not icon.split(".")[-1] in picture_allow_mode:
                raise ValidationError("图片格式不允许！")

    name = StringField(
        "预告标题",
        [
            validators.DataRequired("请填写预告标题吧！"),
            validata_name,
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预告标题",
            "maxlength": "10",
        }
    )
    logo = FileField(
        "预告封面",
        [
            validators.DataRequired("请选择预告封面"),
            validata_logo,
        ],
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary",
        }
    )

class EditPreviewForm(FlaskForm):
    def validata_logo(self, field):
        if type(field.data) != str:
            icon = field.data.filename
            if not icon.split(".")[-1] in picture_allow_mode:
                raise ValidationError("图片格式不允许！")

    name = StringField(
        "预告标题",
        [
            validators.DataRequired("请填写预告标题吧！"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预告标题",
            "maxlength": "10",
        }
    )
    logo = FileField(
        "预告封面",
        [
            validata_logo,
        ],
    )
    submit = SubmitField(
        "修改",
        render_kw={
            "class": "btn btn-primary",
        }
    )


class AuthForm(FlaskForm):
    def validata_name(self, field):
        name = field.data
        if Auth.query.filter_by(name=name).count() == 1:
            raise ValidationError("权限名称已重复！")

    name = StringField(
        "权限名称",
        [
            validators.DataRequired("请填写权限名称"),
            validata_name,
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限名称",
        }
    )
    url = StringField(
        "权限地址",
        [
            validators.DataRequired("请填写权限地址"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址",
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary",
        }
    )


class EditAuthForm(FlaskForm):
    name = StringField(
        "权限名称",
        [
            validators.DataRequired("请填写权限名称"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限名称",
        }
    )
    url = StringField(
        "权限地址",
        [
            validators.DataRequired("请填写权限地址"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址",
        }
    )
    submit = SubmitField(
        "修改",
        render_kw={
            "class": "btn btn-primary",
        }
    )


class AdminForm(FlaskForm):
    def validata_name(self, field):
        name = field.data
        if Admin.query.filter_by(account=name).count() == 1:
            raise ValidationError("权限名称已重复！")

    name = StringField(
        "管理员名称",
        [
            validators.DataRequired("请填写管理员名称！"),
            validata_name,
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称",
            "autofocus": "",
        }
    )
    password = PasswordField(
        "管理员密码",
        [
            validators.DataRequired("密码不能为空！"),
            validators.Length(min=5, max=20, message="密码长度在5至20之间！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "管理员密码",
            "autofocus": "",
        },
    )
    re_password = PasswordField(
        "管理员重复密码",
        [
            validators.DataRequired("密码不能为空！"),
            validators.Length(min=5, max=20, message="密码长度在5至20之间！"),
            validators.EqualTo("password", message="两次输入密码不一致！"),
        ],
        description="确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "管理员重复密码",
            "autofocus": "",
        },
    )
    role = SelectField(
        "所属角色",
        [
            validators.DataRequired("请选择！")],
        coerce=int,
        choices=[],
        render_kw={
            "class": "form-control",
        },
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary",
        }
    )



class PasswordForm(FlaskForm):
    password = PasswordField(
        "旧密码",
        [validators.DataRequired("请输入密码！"),
         validators.Length(max=20, message="密码长度应在5位以上！")
         ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码",
            "autofocus": "",
        }
    )
    new_password = PasswordField(
        "新密码",
        [validators.DataRequired("请输入密码"),
         validators.Length(max=20, message="密码长度应在5位以上！")
         ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码",
            "autofocus": "",
        }
    )
    submit = SubmitField(
        "修改密码",
        render_kw={
            "class": "btn btn-primary",
        },
    )