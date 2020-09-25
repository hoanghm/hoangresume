from app import db
from flask_login import UserMixin, AnonymousUserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import abort

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512))
    image_link = db.Column(db.String(1024))
    short_description = db.Column(db.Text)
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Project %r>' % self.title

class Permission:
    guest = 1
    mod = 2
    admin = 3

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    permission = db.Column(db.Integer)

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        Roles = {'Guest':1, 'Mod':2, 'Admin':3}
        for role in Roles:
            cur_role = Role.query.filter_by(name=role).first()
            if cur_role is None:
                cur_role = Role(name=role, permission=Roles[role])
                db.session.add(cur_role)
                db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(2048))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role.permission == Permission.admin

    @staticmethod
    def insert_admin():
        admin = Role.query.filter_by(name='Admin').first().users.first()
        if admin is None:
            admin_role = Role.query.filter_by(name='Admin').first()
            admin = User(username='admin', password='admin', role=admin_role)
            db.session.add(admin)
            db.session.commit()

class AnonymousUser(AnonymousUserMixin):

    def is_admin(self):
        return False




'''
Authentication decorators
'''

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role.permission >= permission:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.admin)(f)






