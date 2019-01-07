from app.db_sqlalchemy import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255))
    telephone = db.Column(db.String(11))
    username = db.Column(db.String(30))
    password = db.Column(db.String(128))
    icon = db.Column(db.String(64))
    info = db.Column(db.String(128))
    register_time = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255))
    status = db.Column(db.String(10), default="0")



class Login_log(db.Model):
    __tablename__ = "login_log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(255))
    time = db.Column(db.DateTime, index=True, default=datetime.now)
    user = db.relationship('User', backref='login_log')


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    login_logs = db.relationship('Movie', backref='tag')


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    info = db.Column(db.Text)
    star = db.Column(db.Integer)
    play_number = db.Column(db.BigInteger, default=0)
    comment_number = db.Column(db.BigInteger, default=0)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    area = db.Column(db.String(255))
    release_time = db.Column(db.String(255))
    length = db.Column(db.String(255))
    create_time = db.Column(db.Date, default=datetime.now)




class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    logo = db.Column(db.String(255))


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    user = db.relationship('User', backref='comment')
    movie = db.relationship('Movie', backref='comment')


class Movie_collection(db.Model):
    __tablename__ = "movie_collection"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    movie = db.relationship('Movie', backref='movie_collection')
    user = db.relationship('User', backref='movie_collection')



class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    url = db.Column(db.String(255))


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    auths = db.Column(db.Text)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)



class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(255))
    password = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    grade = db.Column(db.String(10), default="普通管理员")
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='admin')


class Admin_Login_log(db.Model):
    __tablename__ = "admin_login_log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(255))
    time = db.Column(db.DateTime, index=True, default=datetime.now)
    admin = db.relationship('Admin', backref='admin_login_log')


class Action_log(db.Model):
    __tablename__ = "action_log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(255))
    time = db.Column(db.DateTime, index=True, default=datetime.now)
    action = db.Column(db.String(255))
    admin = db.relationship('Admin', backref='action_log')