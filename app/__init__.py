from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config
from flask_cors import CORS

mail = Mail()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    CORS(app, origins="*", supports_credentials=True, allow_headers="authorization,content-type")
    # CORS(app, resources=r'/*')
    db.init_app(app)
    mail.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .test import test as test_blueprint
    app.register_blueprint(test_blueprint)

    return app
