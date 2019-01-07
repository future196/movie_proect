from flask import session, redirect, url_for, render_template, request, abort
from functools import wraps
from app.models import Auth, Admin, Role

# wraper 是防止丢失原来的函数属性，可以多次调用

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username"):
            return func(*args, **kwargs)
        else:
            return redirect("/login")
    return wrapper

def admin_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("admin_id"):
            return func(*args, **kwargs)
        else:
            return redirect("/admin/login")
    return wrapper


def admin_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if Admin.query.get(session["admin_id"]).grade == "超级管理员":
            return func(*args, **kwargs)
        else:
            auths = Admin.query.get(session["admin_id"]).role.auths.split(",")[:-1]
            auth_list = [Auth.query.filter(Auth.name == au)[0].url for au in auths]
            auths = [au.url for au in Auth.query.all()]
            if str(request.url_rule) not in auths:
                return func(*args, **kwargs)
            else:
                if str(request.url_rule) in auth_list:
                    return func(*args, **kwargs)
                else:
                    return "您没有权限访问！"
    return wrapper


# auths = Admin.query.get(session["admin_id"]).role.auths.split(",")[:-1]
# auth_list = []
# for au in auths:
#     auth_list.append(Auth.query.filter(Auth.name == au)[0].url)
# auths = []
# for au in Auth.query.all():
#     auths.append(au.url)
