from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.db_sqlalchemy import db
from app import app

db.init_app(app)
manager = Manager(app)
migrate = Migrate(app=app, db=db)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
