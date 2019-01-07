from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint
from app import settings

from flask import Flask

from app.models import User, Login_log
app = Flask(__name__)
app.debug = settings.debug
app.config.from_object(settings)
app.config['SECRET_KEY'] = "05656895978645d5bc9dc78410f22382"
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(home_blueprint)


