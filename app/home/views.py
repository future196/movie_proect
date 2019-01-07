from app.home import home
from flask import render_template, redirect, flash, session, request, json
from app.home.form import RegisterForm, LoginForm, UserForm, PasswordForm
from hashlib import md5
from app.models import User, Login_log, Tag, Movie, Comment, Movie_collection, Preview
import uuid
from app.db_sqlalchemy import db
from app.decorators import login_required
from app import settings
import os
from sqlalchemy import and_


@home.route("/")
def index():
    page = request.args.get("page", 1)
    tag = request.args.get("tag")
    star = request.args.get("star")
    data = request.args.get("year")
    play = request.args.get("play")
    comment = request.args.get("comment")
    previews = Preview.query.all()
    if tag:
        paginate = Movie.query.filter_by(tag_id=tag).paginate(page=int(page), per_page=16)
    elif star:
        paginate = Movie.query.filter_by(star=star).paginate(page=int(page), per_page=16)
    elif data:
        if data == "new":
            paginate = Movie.query.filter_by().order_by("-create_time").paginate(page=int(page), per_page=16)
        elif data == "old":
            paginate = Movie.query.filter(Movie.create_time == "2018",Movie.create_time == "2017",Movie.create_time == "2016",).paginate(page=int(page), per_page=16)
        else:
            paginate = Movie.query.filter(Movie.create_time.like(data + "%")).paginate(page=int(page), per_page=16)
    elif play:
        if play == "high":
            paginate = Movie.query.filter_by().order_by("-play_number").paginate(page=int(page), per_page=16)
        else:
            paginate = Movie.query.filter_by().order_by("play_number").paginate(page=int(page), per_page=16)
    elif comment:
        if comment == "high":
            paginate = Movie.query.filter_by().order_by("-comment_number").paginate(page=int(page), per_page=16)
        else:
            paginate = Movie.query.filter_by().order_by("comment_number").paginate(page=int(page), per_page=16)
    else:
        paginate = Movie.query.filter_by().paginate(page=int(page), per_page=16)
    tags = Tag.query.all()
    content = {
        "tags": tags,
        "paginate": paginate,
        "preview": previews[0],
        "previews": previews[1:],
    }
    return render_template("movie/index.html", **content)  # 传输字典的时候需要加**


@home.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        m = md5()
        m.update(bytes(data["password"], encoding="utf-8"))  # 加密前必须先编码
        password = m.hexdigest()
        user = User(
            email=data["email"],
            telephone=data["telephone"],
            username=data["username"],
            password=password,
            icon="default.jpg",
            uuid=uuid.uuid4().hex,
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("movie/register.html", form=form)


@home.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        account = data["username"]
        m = md5()
        m.update(bytes(data["password"], encoding="utf-8"))  # 加密前必须先编码
        password = m.hexdigest()
        if account.isdigit() and len(account) == 11:
            user = User.query.filter_by(telephone=account).count()
            if user == 1:
                if User.query.filter_by(telephone=account).first().password == password:
                    session["username"] = User.query.filter_by(telephone=account).first().username
                    session["userid"] = User.query.filter_by(telephone=account).first().id
                    session.permanent = True

                    # 生成登录日志
                    login_log = Login_log(user_id=session["userid"], ip=request.remote_addr)
                    db.session.add(login_log)
                    db.session.commit()
                    return redirect("/")
                else:
                    flash("密码错误", "password_error")
            else:
                flash("账号不存在！", "account_error")

        elif "@" in account:
            user = User.query.filter_by(email=account).count()
            if user == 1:
                if User.query.filter_by(email=account).first().password == password:
                    session["username"] = User.query.filter_by(email=account).first().username
                    session["userid"] = User.query.filter_by(email=account).first().id
                    session.permanent = True

                    # 生成登录日志
                    login_log = Login_log(user_id=session["userid"], ip=request.remote_addr)
                    db.session.add(login_log)
                    db.session.commit()
                    return redirect("/")
                else:
                    flash("密码错误", "password_error")
            else:
                flash("账号不存在！", "account_error")
        else:
            user = User.query.filter_by(username=account).count()
            if user == 1:
                if User.query.filter_by(username=account).first().password == password:
                    session["username"] = User.query.filter_by(username=account).first().username
                    session["userid"] = User.query.filter_by(username=account).first().id
                    session.permanent = True

                    # 生成登录日志
                    login_log = Login_log(user_id=session["userid"], ip=request.remote_addr)
                    db.session.add(login_log)
                    db.session.commit()
                    return redirect("/")
                else:
                    flash("密码错误", "password_error")
            else:
                flash("账号不存在！", "account_error")

    return render_template("movie/login.html", form=form)


@home.route("/user_info", methods=["GET", "POST"])
@login_required
def user_info():
    form = UserForm()
    user = User.query.filter_by(username=session["username"]).first()
    if request.method == "GET":
        form.username.data = user.username
        form.email.data = user.email
        form.telephone.data = user.telephone
        form.info.data = user.info
        form.icon.data = user.icon
    elif request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            username = data["username"]
            telephone = data["telephone"]
            info = data["info"]
            icon = data["icon"]
            email = data["email"]
            if type(icon) == str:
                filename = user.icon
            else:
                filename = icon.filename
                filename = str(session["userid"]) + "." + "jpg"
                icon.save(os.path.join(settings.user_icon_path, filename))
            user.username = username
            user.telephone = telephone
            user.info = info
            user.email = email
            user.icon = filename
            db.session.commit()
            return redirect("/user_info")
    content = {
        "form": form,
        "icon": user.icon,
    }
    return render_template("movie/user.html", **content)


@home.route("/user_comments")
@login_required
def user_comments():
    page = request.args.get("page", 1)
    paginate = Comment.query.filter_by(user_id=session["userid"]).order_by("-create_time").paginate(page=int(page),
                                                                                                    per_page=5)
    content = {
        "paginate": paginate,
    }
    return render_template("movie/comments.html", **content)


@home.route("/user_movie_collection")
@login_required
def movie_collection():
    page = request.args.get("page", 1)
    paginate = Movie_collection.query.filter_by(user_id=session["userid"]).order_by("-create_time").paginate(
        page=int(page), per_page=5)
    content = {
        "paginate": paginate,
    }
    return render_template("movie/moviecol.html", **content)


@home.route("/user_password", methods=["GET", "POST"])
@login_required
def user_password():
    form = PasswordForm()
    if request.method == "POST":
        user = User.query.filter_by(id=session["userid"]).first()
        data = form.data
        m = md5()
        m.update(bytes(data["password"], encoding="utf-8"))
        password = m.hexdigest()
        m2 = md5()
        m2.update(bytes(data["new_password"], encoding="utf-8"))
        new_password = m2.hexdigest()
        if password == user.password:
            user.password = new_password
            db.session.add(user)
            db.session.commit()
            flash("修改成功！", "change_success")
        else:
            flash("原密码错误！", "change_failed")
    return render_template("movie/pwd.html", form=form)


@home.route("/user_login_log")
@login_required
def login_log():
    page = request.args.get("page", 1)
    paginate = Login_log.query.filter_by(user_id=session["userid"]).order_by(Login_log.id.desc()).paginate(
        page=int(page), per_page=5)
    return render_template("movie/loginlog.html", paginate=paginate)


@home.route("/search")
def search():
    data = request.args.get("data")
    page = request.args.get("page", 1)
    paginate = Movie.query.filter(Movie.name.like("%" + data + "%")).paginate(page=page, per_page=5)
    content = {
        "paginate": paginate,
        "data": data,
    }
    return render_template("movie/search.html", **content)


@home.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@home.route("/play")
def play():
    page = request.args.get("page", 1)
    movie_id = request.args.get("movie")
    movie = Movie.query.get(int(movie_id))
    tag_name = Tag.query.get(movie.tag_id).name
    paginate = Comment.query.filter_by(movie_id=movie_id).order_by("-create_time").paginate(page=int(page), per_page=10)
    obj = Movie.query.get(movie_id)
    obj.play_number = obj.play_number + 1
    db.session.add(obj)
    db.session.commit()
    content = {
        "movie": movie,
        "tag_name": tag_name,
        "paginate": paginate,
    }
    return render_template("movie/play.html", **content)


@home.route("/comment")
def comment():
    id = request.args.get("movie")
    content = request.args.get("content")
    comment = Comment(user_id=session["userid"], movie_id=id, content=content)
    obj = Movie.query.get(id)
    obj.comment_number = obj.comment_number + 1
    db.session.add(obj)
    db.session.add(comment)
    db.session.commit()
    context = {
        "status": "评论成功！",
        "content": comment.content,
        "username": comment.user.username,
        "create_time": str(comment.create_time),
        "user_icon": comment.user.icon,
        "comment_number": obj.comment_number,
    }
    return json.dumps(context, ensure_ascii=False)


@home.route("/add_movie_collection")
def add_movie_collection():
    movie_id = request.args.get("movie")
    movie_col = Movie_collection(movie_id=movie_id, user_id=session["userid"])
    db.session.add(movie_col)
    db.session.commit()
    content = {
        "status": "已收藏",
    }
    return json.dumps(content, ensure_ascii=False)
