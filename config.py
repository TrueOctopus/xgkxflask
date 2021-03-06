# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zxcvbnm123'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.exmail.qq.com'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN') or '18368876370@163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') or 'xgkx@hguxgkx.com'
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') or 'Zdhnb666'
    MAIL_DEFAULT_SENDER = (os.getenv('MAIL_USERNAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + \
                              os.path.join(basedir, 'Dev-user.sqlite')


class TestingConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + \
                              os.path.join(basedir, 'Pro-user.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
