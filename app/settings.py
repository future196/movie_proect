import os

DIALECT = "mysql"
DRIVER = "pymysql"
HOSTNAME = "localhost"
PORT = "3306"
USERNAME = "root"
PASSWORD = "root"
DATABASE = "movie"

format = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = format

SQLALCHEMY_TRACK_MODIFICATIONS = True

debug = True

user_icon_path = os.getcwd() + "/app/static/img/user_icon/"
video_logo_path = os.getcwd() + "/app/static/img/logo/"
preview_logo_path = os.getcwd() + "/app/static/img/preview/"
video_path = os.getcwd() + "/app/static/video/"
icon_allow_mode = ["jpg", "png", "jpeg", "gif", "tiff", "tif", "bmp", "jfif"]
picture_allow_mode = ["jpg", "png", "jpeg", "gif", "tiff", "tif", "bmp", "jfif"]
movie_allow_mode = ["avi", "wmv", "mpeg", "mp4", "mov", "mkv", "flv", "f4v", "m4v", "rmvb", "rm", "3gp", ]
