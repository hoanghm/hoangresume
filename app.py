from flask import Flask
import os
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


# config
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "asecretkey"
    # SECRET_KEY = 'default'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    RESUME_LINK = os.environ.get("RESUME_LINK")
    MAIL_DEFAULT_SENDER = 'hoanghm4@gmail.com'


'''
Initialize the app
'''
app = Flask(__name__)
app.config.from_object(Config)

mail = Mail()
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()

mail.init_app(app)
db.init_app(app)
bootstrap.init_app(app)
login_manager.init_app(app)

from main.models import User, AnonymousUser
login_manager.session_protection = 'strong'
login_manager.login_view = 'page.login'
login_manager.anonymous_user = AnonymousUser
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


manager = Manager(app)
migrate = Migrate(app, db)
def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context()))
manager.add_command("db", MigrateCommand)

@manager.command
def deploy():
    from flask_migrate import upgrade
    from main.models import User, Role
    upgrade()
    Role.insert_roles()
    User.insert_admin()

'''
connect with views
'''
from main import page as page_blueprint
app.register_blueprint(page_blueprint)


if __name__ == '__main__':
    manager.run()
