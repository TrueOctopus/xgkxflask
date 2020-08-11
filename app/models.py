# -*- coding: utf-8 -*-
from flask import current_app
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from . import default_img


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)  # id
    username = db.Column(db.String(15), unique=True)  # 昵称
    name = db.Column(db.String(64))  # 姓名
    profile_photo = db.Column(db.Text(), default=default_img)  # 头像
    sex = db.Column(db.Integer)  # 性别
    grade = db.Column(db.String(64))  # 年级
    college = db.Column(db.String(64))  # 学院
    major = db.Column(db.String(64))  # 专业
    student_num = db.Column(db.String(12), unique=True, index=True)  # 学号
    phone_num = db.Column(db.String(11), unique=True)  # 电话
    email = db.Column(db.String(64), unique=True, index=True)  # 邮箱地址
    password_hash = db.Column(db.String(128))  # 密码
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

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def generate_changePwd_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'pwd': self.id}).decode('utf-8')

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

    def forgetPwdConfirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('pwd') != self.id:
            return False
        return True

    # def generate_auth_token(self, expiration):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    #     return s.dumps({'id': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return None
    #     return User.query.get(data['id'])
    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'profile_photo': self.profile_photo,
            'sex': self.sex,
            'college': self.college,
            'major': self.major,
            'grade': self.grade,
            'student_num': self.student_num,
            'phone_num': self.phone_num,
            'email': self.email,
            'about_me': self.about_me,
            'confirmed': self.confirmed
        }
        return json_user


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)  # id
    art_type = db.Column(db.String(64), index=True)  # 文章类型（activity或notice）
    title = db.Column(db.String(64), unique=True, index=True)  # 标题
    body = db.Column(db.Text)  # 正文
    timestamp = db.Column(db.String(64), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 时间戳

    def to_json(self):
        json_user = {
            'id': self.id,
            'art_type': self.art_type,
            'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp
        }
        return json_user

    def to_json_nobody(self):
        json_user = {
            'id': self.id,
            'art_type': self.art_type,
            'title': self.title,
            'timestamp': self.timestamp
        }
        return json_user
