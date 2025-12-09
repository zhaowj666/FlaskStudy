from .extensions import db
from datetime import datetime, UTC
from werkzeug.security import generate_password_hash, check_password_hash


user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

role_permission = db.Table(
    'role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column('password', db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # 关联关系
    roles = db.relationship('Role', secondary=user_role, backref='users')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name):
        for role in self.roles:
            for perm in role.permissions:
                if perm.name == permission_name:
                    return True
        return False


    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    # 关联关系
    permissions = db.relationship('Permission', secondary=role_permission, backref='roles')

    def __repr__(self):
        return '<Role %r>' % self.name


class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)


    def __repr__(self):
        return '<Permission %r>' % self.name


class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(64), nullable=False, default='info')
    request_id = db.Column(db.String(128), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)

    def __repr__(self):
        return '<Logs %r>' % self.level

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'request_id': self.request_id,
            'message': self.message,
            'created_at': self.created_at,
        }

class Permissions:
    USER_READ  = 'user:read'
    USER_WRITE = 'user:write'
    ADMIN_READ = 'admin:read'
    ADMIN_WRITE = 'admin:write'

