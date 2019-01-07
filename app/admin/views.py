from app.admin import admin
from flask import render_template, session, redirect, flash, request, json
from app.admin.form import LoginForm, TagAddForm, MovieForm, PreviewForm, AuthForm, AdminForm, EditMovieForm,\
    EditTagForm, EditPreviewForm, EditAuthForm, PasswordForm
from app.models import Admin, Tag, Movie, Preview, User, Comment, Movie_collection, Admin_Login_log, Login_log, \
    Action_log, Auth, Role
from hashlib import md5
from app.decorators import admin_login_required, admin_auth
import datetime
from app.db_sqlalchemy import db
import os
from app.settings import video_path, video_logo_path, preview_logo_path


@admin.route("/")
@admin_login_required
def index():
    data = str(datetime.datetime.now()).split(" ")[0]
    return render_template("admin/index.html", data=data)


@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = Admin.query.filter_by(account=data["account"])
        if user.count() == 1:
            m = md5()
            m.update(bytes(data["password"], encoding="utf-8"))
            password = m.hexdigest()
            if user.first().password == password:
                session["admin_id"] = user.first().id
                session["admin_name"] = user.first().account
                login_log = Admin_Login_log(admin_id=session["admin_id"], ip=request.remote_addr)
                db.session.add(login_log)
                db.session.commit()
                flash("", "error")
                return redirect("/admin")
            else:
                flash("密码错误！", "error")
        else:
            flash("账号不存在！", "error")
    return render_template("admin/login.html", form=form)


@admin.route("/tag_add", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def tag_add():
    form = TagAddForm()
    if form.validate_on_submit():
        data = form.data
        if Tag.query.filter_by(name=data["tag"]).count() == 1:
            flash("标签重复！", "error")
        else:
            tag = Tag(name=data["tag"])

            # 添加操作日志
            action = "添加了一个标签：" + data["tag"]
            action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
            db.session.add(action_log)

            db.session.add(tag)
            db.session.commit()
            flash("添加成功！", "success")

    return render_template("admin/tag_add.html", form=form)


@admin.route("/tag_modify", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def tag_modify():
    target = request.args.get("target", "00")
    if target == "00":
        return "404"
    tag = Tag.query.get(target)
    form = EditTagForm()
    if request.method == "GET":
        form.tag.data = tag.name
    if form.validate_on_submit():
        data = form.data
        if data["tag"] != tag.name:
            if Tag.query.filter_by(name=data["tag"]).count() == 0:

                # 添加操作日志
                action = "标签“" + tag.name + "”被修改为“" + data["tag"] + "”"
                action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
                tag.name = data["tag"]
                db.session.add(action_log)
                db.session.add(tag)
                db.session.commit()
                flash("修改成功！", "status")
            else:
                flash("标签已存在！", "status")
        else:
            flash("修改成功！", "status")
    return render_template("admin/tag_modify.html", form=form)


@admin.route("/tag_list")
@admin_login_required
def tag_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Tag.query.filter(Tag.name.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=10)
    return render_template("admin/tag_list.html", paginate=paginate)


@admin.route("/tag_del")
@admin_login_required
@admin_auth
def tag_del():
    target = request.args.get("target")
    tag = Tag.query.get(target)

    # 添加操作日志
    action = "删除了一个标签：" + tag.name
    action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
    db.session.add(action_log)
    db.session.delete(tag)
    db.session.commit()
    context = {
        "status": "删除成功！",
    }
    return json.dumps(context, ensure_ascii=False)


@admin.route("/movie_add", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def movie_add():
    form = MovieForm()
    form.tag.choices = [(tag.id, tag.name) for tag in Tag.query.filter_by()]
    if form.validate_on_submit():
        data = form.data
        movie_name = data["name"] + "." + form.movie.data.filename.split(".")[-1]
        logo_name = data["name"] + "." + form.logo.data.filename.split(".")[-1]
        if data["length"] >= 60 and data["length"] < 3600:
            minutes = data["length"] // 60
            seconds = data["length"] % 60
            length = str(minutes) + "分" + str(seconds) + "秒"
        elif data["length"] < 60:
            length = str(data["length"]) + "秒"
        elif data["length"] >= 3600:
            hours = data["length"] // 3600
            minutes = (data["length"] % 3600) // 60
            seconds = data["length"] % 60
            length = str(hours) + "小时" + str(minutes) + "分" + str(seconds) + "秒"
        data["movie"].save(os.path.join(video_path, movie_name))
        data["logo"].save(os.path.join(video_logo_path, logo_name))
        movie = Movie(name=data["name"], info=data["content"], area=data["area"], tag_id=data["tag"],
                      length=length, release_time=data["release_time"], star=int(data["star"]), logo=logo_name,
                      url=movie_name)
        # 添加操作日志
        action = "添加了一个视频：" + data["name"]
        action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
        db.session.add(action_log)
        db.session.add(movie)
        db.session.commit()
        flash("添加成功！", "success")
    return render_template("admin/movie_add.html", form=form)


@admin.route("/movie_modify", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def movie_modify():
    target = request.args.get("target")
    form = EditMovieForm()
    movie = Movie.query.get(target)
    form.tag.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            ispass = ""
            if data["name"] != movie.name:
                if Movie.query.filter_by(name=data["name"]).count() == 0:
                    movie.name = data["name"]
                else:
                    ispass = "2"
                    flash("片名已重复！")
            if ispass != "2":
                if data["movie"]:
                    movie_name = data["name"] + "." + form.movie.data.filename.split(".")[-1]
                    data["movie"].save(os.path.join(video_path, movie_name))
                    movie.url = movie_name
                if data["logo"]:
                    logo_name = data["name"] + "." + form.logo.data.filename.split(".")[-1]
                    if os.path.exists(video_logo_path + movie.url):
                        os.remove(video_logo_path + movie.url)
                    data["logo"].save(os.path.join(video_logo_path, logo_name))
                    movie.logo = logo_name
                if data["content"] != movie.info:
                    movie.info = data["content"]
                if data["star"] != movie.star:
                    movie.star = data["star"]
                if data["tag"] != movie.tag:
                    movie.tag_id = data["tag"]
                if data["area"] != movie.area:
                    movie.area = data["area"]
                if data["release_time"] != movie.release_time:
                    movie.release_time = data["release_time"]
                if data["length"] >= 60 and data["length"] < 3600:
                    minutes = data["length"] // 60
                    seconds = data["length"] % 60
                    length = str(minutes) + "分" + str(seconds) + "秒"
                elif data["length"] < 60:
                    length = str(data["length"]) + "秒"
                elif data["length"] >= 3600:
                    hours = data["length"] // 3600
                    minutes = (data["length"] % 3600) // 60
                    seconds = data["length"] % 60
                    length = str(hours) + "小时" + str(minutes) + "分" + str(seconds) + "秒"
                if length != movie.length:
                    movie.length = length
                # 添加操作日志
                action = "修改了一个视频：" + data["name"]
                action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
                db.session.add(action_log)
                db.session.add(movie)
                db.session.commit()
                flash("修改成功！", "success")

    elif request.method == "GET":
        form.name.data = movie.name
        form.content.data = movie.info
        form.star.data = movie.star
        form.tag.data = movie.tag_id
        form.area.data = movie.area
        if "小时" in movie.length:
            hour = movie.length.split("小时")[0]
            minutes = movie.length.split("小时")[1].split("分")[0]
            seconds = movie.length.split("小时")[1].split("分")[1].split("秒")[0]
            length = int(hour)*3600 + int(minutes)*60 + int(seconds)
        elif "分" in movie.length:
            minutes = movie.length.split("分")[0]
            seconds = movie.length.split("分")[1].split("秒")[0]
            length = int(minutes) * 60 + int(seconds)
        elif "秒" in movie.length:
            seconds = movie.length.split("秒")[0]
            length = int(seconds)
        form.length.data = length
        form.release_time.data = movie.release_time
    content = {
        "form": form,
        "logo": movie.logo,
    }

    return render_template("admin/movie_modify.html", **content)


@admin.route("/movie_list", methods=["GET", "POST"])
@admin_login_required
def movie_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Movie.query.filter(Movie.name.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=10)
    return render_template("admin/movie_list.html", paginate=paginate)


@admin.route("/movie_del")
@admin_login_required
def movie_del():
    target = request.args.get("target")
    movie = Movie.query.get(target)

    # 添加操作日志
    action = "删除了一个视频：" + movie.name
    action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
    db.session.add(action_log)
    db.session.delete(movie)
    if os.path.exists(video_logo_path + movie.url):
        os.remove(video_logo_path + movie.url)
    db.session.commit()
    context = {
        "status": "删除成功！",
    }
    return json.dumps(context, ensure_ascii=False)


@admin.route("/preview_add", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        preview_name = data["name"] + "." + data["logo"].filename.split(".")[-1]
        data["logo"].save(os.path.join(preview_logo_path, preview_name))
        preview = Preview(name=data["name"], logo=preview_name)
        # 添加操作日志
        action = "添加了一个预告：" + data["name"]
        action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
        db.session.add(action_log)
        db.session.add(preview)
        db.session.commit()
        flash("添加成功！", "status")
    return render_template("admin/preview_add.html", form=form)


@admin.route("/preview_modify", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def preview_modify():
    target = request.args.get("target")
    form = EditPreviewForm()
    preview = Preview.query.get(target)
    if request.method == "GET":
        form.name.data = preview.name
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            ispass = ""
            if data["name"] != preview.name:
                if Preview.query.filter_by(name=data["name"]).count() == 0:
                    preview.name = data["name"]
                else:
                    ispass = "00"
                    flash("预告标题已存在！", "name_error")
            if ispass != "00":
                if data["logo"]:
                    logo_name = data["name"] + "." + form.logo.data.filename.split(".")[-1]
                    if os.path.exists(preview_logo_path + preview.logo):
                        os.remove(preview_logo_path + preview.logo)
                    data["logo"].save(os.path.join(preview_logo_path, logo_name))
                    preview.logo = logo_name
            # 添加操作日志
            action = "修改了一个预告：" + data["name"]
            action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
            db.session.add(action_log)
            db.session.add(preview)
            db.session.commit()
            flash("修改成功！", "status")

    content = {
        "form": form,
        "logo": preview.logo,
    }
    return render_template("admin/preview_modify.html", **content)

@admin.route("/preview_list")
@admin_login_required
def preview_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Preview.query.filter(Preview.name.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=5)
    content = {
        "paginate": paginate,
    }
    return render_template("admin/preview_list.html", **content)


@admin.route("/preview_del")
@admin_login_required
@admin_auth
def preview_del():
    target = request.args.get("target")
    preview = Preview.query.get(target)

    # 添加操作日志
    action = "删除了一个预告：" + preview.name
    action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
    db.session.add(action_log)
    db.session.delete(preview)
    if os.path.exists(preview_logo_path + preview.logo):
        os.remove(preview_logo_path + preview.logo)
    db.session.commit()
    context = {
        "status": "删除成功！",
    }
    return json.dumps(context, ensure_ascii=False)


@admin.route("/user_list")
@admin_login_required
def user_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = User.query.filter(User.username.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=5)
    content = {
        "paginate": paginate,
    }
    return render_template("admin/user_list.html", **content)


@admin.route("/user_del")
@admin_login_required
@admin_auth
def user_del():
    target = request.args.get("target")
    user = User.query.get(target)

    # 添加操作日志
    action = "删除了一个会员：" + user.username
    action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
    db.session.add(action_log)
    db.session.delete(user)
    db.session.commit()
    context = {
        "status": "删除成功！",
    }
    return json.dumps(context, ensure_ascii=False)


@admin.route("/user_view")
@admin_login_required
def user_view():
    target = request.args.get("target")
    user = User.query.get(target)
    content = {
        "user": user,
    }
    return render_template("admin/user_view.html", **content)


@admin.route("/user_frost")
@admin_login_required
@admin_auth
def user_frost():
    target = request.args.get("target")
    user = User.query.get(target)
    user.status = "0"
    # 添加操作日志
    action = "冻结了一个会员：" + user.username
    action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
    db.session.add(action_log)
    db.session.add(user)
    db.session.commit()
    context = {
        "status": "冻结成功！",
    }
    return json.dumps(context, ensure_ascii=False)


@admin.route("/user_recover")
@admin_login_required
@admin_auth
def user_recover():
    target = request.args.get("target")
    user = User.query.get(target)
    user.status = "1"
    # 添加操作日志
    action = "恢复了一个被冻结的会员：" + user.username
    action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
    db.session.add(action_log)
    db.session.add(user)
    db.session.commit()
    context = {
        "status": "解冻成功！",
    }
    return json.dumps(context, ensure_ascii=False)


@admin.route("/comment_list")
@admin_login_required
def comment_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Comment.query.filter(Comment.content.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=6)
    content = {
        "paginate": paginate,
    }
    return render_template("admin/comment_list.html", **content)


@admin.route("/comment_del")
@admin_login_required
@admin_auth
def comment_del():
    target = request.args.get("target")
    comment = Comment.query.get(target)
    movie = Movie.query.get(comment.movie.id)
    movie.comment_number = movie.comment_number - 1
    # 添加操作日志
    action = "删除了一个 " + comment.user.username + " 的评论：" + comment.content
    action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
    db.session.add(action_log)
    db.session.delete(comment)
    db.session.add(movie)
    db.session.commit()
    context = {
        "status": "删除成功！",
    }
    return json.dumps(context, ensure_ascii=False)


@admin.route("/moviecol_list")
@admin_login_required
def moviecol_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Movie_collection.query.filter(Movie_collection.content.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=10)
    content = {
        "paginate": paginate,
    }
    return render_template("admin/moviecol_list.html", **content)


@admin.route("/moviecol_del")
@admin_login_required
@admin_auth
def moviecol_del():
    target = request.args.get("target")
    collection = Movie_collection.query.get(target)

    # 添加操作日志
    action = "删除了一个 " + collection.user.username + " 的收藏：" + collection.movie.name
    action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
    db.session.add(action_log)
    db.session.delete(collection)
    db.session.commit()
    context = {
        "status": "删除成功！",
    }
    return json.dumps(context, ensure_ascii=False)


@admin.route("/log_list")
@admin_login_required
def log_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Action_log.query.filter(Action_log.action.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=10)
    content = {
        "paginate": paginate,
    }
    return render_template("admin/log_list.html", **content)


@admin.route("/admin_login_log_list")
@admin_login_required
def admin_login_log_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Admin_Login_log.query.filter(Admin_Login_log.ip.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=10)
    content = {
        "paginate": paginate,
    }
    return render_template("admin/adminloginlog_list.html", **content)


@admin.route("/user_login_log_list")
@admin_login_required
def user_login_log_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Login_log.query.filter(Login_log.ip.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=10)
    content = {
        "paginate": paginate,
    }
    return render_template("admin/userloginlog_list.html", **content)


@admin.route("/auth_add", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(name=data["name"], url=data["url"])

        # 添加操作日志
        action = "添加了一个权限：" + data["name"]
        action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
        db.session.add(action_log)

        db.session.add(auth)
        db.session.commit()
        flash("添加成功！", "status")
    return render_template("admin/auth_add.html", form=form)


@admin.route("/auth_modify", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def auth_modify():
    target = request.args.get("target")
    auth = Auth.query.get(target)
    form = EditAuthForm()
    if request.method == "GET":
        form.name.data = auth.name
        form.url.data = auth.url
    if request.method == "POST":
        if form.validate_on_submit:
            data = form.data
            ispass = ""
            if data["name"] != auth.name:
                if Auth.query.filter_by(name=data["name"]).count() == 0:
                    auth.name = data["name"]
                else:
                    ispass = "00"
                    flash("权限名称已存在！", "name_error")
            if ispass != "00":
                if data["url"] != auth.url:
                    auth.url = data["url"]
            # 添加操作日志
            action = "修改了一个权限：" + data["name"]
            action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
            db.session.add(action_log)
            db.session.add(auth)
            db.session.commit()
            flash("修改成功！", "status")

    content = {
        "form": form,
    }
    return render_template("admin/auth_modify.html", **content)

@admin.route("/auth_list")
@admin_login_required
def auth_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Auth.query.filter(Auth.name.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=10)
    content = {
        "paginate": paginate,
    }
    return render_template("admin/auth_list.html", **content)



@admin.route("/auth_del")
@admin_login_required
@admin_auth
def auth_del():
    target = request.args.get("target")
    auth = Auth.query.get(target)

    # 添加操作日志
    action = "删除了一个权限：" + auth.name
    action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
    db.session.add(action_log)
    db.session.delete(auth)
    db.session.commit()
    context = {
        "status": "删除成功！",
    }
    return json.dumps(context, ensure_ascii=False)


@admin.route("/role_add", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def role_add():
    auth_list = Auth.query.all()
    if request.method == "POST":
        name = request.form.get("name")
        auth = request.values.getlist("auth")
        if Role.query.filter_by(name=name).count() == 1:
            flash("角色名称已重复！", "error")
        elif len(auth) == 0:
            flash("请选择权限!", "error")
        else:
            auths = ""
            for i in auth:
                auths = auths + i + ","
            role = Role(name=name, auths=auths)

            # 添加操作日志
            action = "添加了一个角色：" + name
            action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
            db.session.add(action_log)
            db.session.add(role)
            db.session.commit()
            flash("添加成功", "error")
    return render_template("admin/role_add.html", auth_list=auth_list)


@admin.route("/role_modify", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def role_modify():
    target = request.args.get("target")
    role = Role.query.get(target)
    if request.method == "POST":
        name = request.form.get("name")
        auth = request.form.getlist("auth")
        auths = ""
        for i in auth:
            auths = auths + i + ","
        ispass = ""
        if name != role.name:
            if Role.query.filter_by(name=name).count() == 0:
                role.name = name
            else:
                ispass = "00"
                flash("角色名称已存在！", "error")
        if ispass != "00":
            if auths != role.auths:
                role.auths = auths
        # 添加操作日志
        action = "修改了一个角色：" + name
        action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
        db.session.add(action_log)
        db.session.add(role)
        db.session.commit()
        flash("修改成功！", "error")
    content = {
        "role": role,
        "auth_list": Auth.query.all(),
        "auth_check": role.auths.split(","),
    }
    return render_template("admin/role_modify.html", **content)


@admin.route("/role_list")
@admin_login_required
def role_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Role.query.filter(Role.name.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=10)
    content = {
        "paginate": paginate,
    }
    return render_template("admin/role_list.html", **content)


@admin.route("/role_del")
@admin_login_required
def role_del():
    target = request.args.get("target")
    role = Role.query.get(target)

    # 添加操作日志
    action = "删除了一个角色：" + role.name
    action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
    db.session.add(action_log)
    db.session.delete(role)
    db.session.commit()
    context = {
        "status": "删除成功！",
    }
    return json.dumps(context, ensure_ascii=False)


@admin.route("/admin_add", methods=["GET", "POST"])
@admin_login_required
@admin_auth
def admin_add():
    form = AdminForm()
    form.role.choices = [(role.id, role.name) for role in Role.query.all()]
    if form.validate_on_submit():
        data = form.data
        name = data["name"]
        role = data["role"]
        password = data["password"]
        m = md5()
        m.update(bytes(password, encoding="utf-8"))
        print(role)
        password = m.hexdigest()
        admin = Admin(account=name, password=password, role_id=role)

        # 添加操作日志
        action = "添加了一个管理员：" + data["name"]
        action_log = Action_log(admin_id=session["admin_id"], ip=request.remote_addr, action=action)
        db.session.add(action_log)
        db.session.add(admin)
        db.session.commit()
        flash("添加成功！", "status")

    return render_template("admin/admin_add.html", form=form)


@admin.route("/admin_list")
@admin_login_required
def admin_list():
    search = request.args.get("search", "")
    page = request.args.get("page", 1)
    paginate = Admin.query.filter(Admin.account.like("%" + search + "%")).order_by("-id").paginate(page=int(page), per_page=10)
    content = {
        "paginate": paginate,
    }
    return render_template("admin/admin_list.html", **content)


@admin.route("/password",methods=["GET", "POST"])
@admin_login_required
def password():
    form = PasswordForm()
    if request.method == "POST":
        user = Admin.query.get(session["admin_id"])
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
            flash("修改成功！", "status")
        else:
            flash("原密码错误！", "status")
    return render_template("admin/pwd.html", form=form)



@admin.route("/logout")
@admin_login_required
def logout():
    session.clear()
    return redirect("/admin/login")
