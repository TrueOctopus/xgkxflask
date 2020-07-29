# -*- coding: utf-8 -*-
from flask import current_app
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # id
    username = db.Column(db.String(64), unique=True, index=True)  # 昵称
    name = db.Column(db.String(64), unique=True, index=True)  # 姓名
    sex = db.Column(db.String(64), index=True)  # 性别
    college = db.Column(db.String(64), index=True)  # 学院
    class_name = db.Column(db.String(64), index=True)  # 班级
    student_num = db.Column(db.String(12), unique=True, index=True)  # 学号
    phone_num = db.Column(db.String(11), unique=True, index=True)  # 电话
    email = db.Column(db.String(64), unique=True, index=True)  # 邮箱地址
    password_hash = db.Column(db.String(128))  # 密码
    location = db.Column(db.String(64))  # 地理位置
    about_me = db.Column(db.Text())  # 个人介绍
    confirmed = db.Column(db.Boolean, default=False)  # 邮箱验证

    @property
    def password(self):
        raise AttributeError('密码未设定')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'sex': self.sex,
            'college': self.college,
            'class_name': self.class_name,
            'student_num': self.student_num,
            'phone_num': self.phone_num,
            'email': self.email,
            'location': self.location,
            'about_me': self.about_me,
            'confirmed': self.confirmed
        }
        return json_user
