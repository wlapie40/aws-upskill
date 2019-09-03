import logging as logger
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from config import (DevelopmentConfig,
                    ProductionConfig,
                    DockerConfig,
                    )
from filters import datetimeformat, file_type
from models import db
from resources import _read_parameters_store
logger.basicConfig(level="DEBUG")


def create_app():
    if os.environ['FLASK_ENV'] == 'prod':
        param_store = _read_parameters_store('sfigiel-prod-db-cred', True)
        config = DevelopmentConfig(*param_store)

    elif os.environ['FLASK_ENV'] == 'dev':
        param_store = _read_parameters_store('sfigiel-dev-db-cred', True)
        config = DevelopmentConfig(*param_store)

    elif os.environ['FLASK_ENV'] == 'docker':
        param_store = _read_parameters_store('sfigiel-docker-db-cred', True)
        config = DevelopmentConfig(*param_store)

    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'the random string'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    logger.debug(f'DATABASE_CONNECTION_URI: {config.DATABASE_CONNECTION_URI}')
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    logger.debug(f'CREATING DB ENGINE ...')
    engine = create_engine(flask_app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)
    logger.debug(f'DATABASE_ENGINE: {database_exists(engine.url)}')

    with flask_app.app_context():
        db.init_app(flask_app)
        db.create_all()
        api = Api(flask_app)
        Bootstrap(flask_app)

        login_manager = LoginManager()
        login_manager.init_app(flask_app)
        login_manager.login_view = 'login'

        flask_app.jinja_env.filters['datetimeformat'] = datetimeformat
        flask_app.jinja_env.filters['file_type'] = file_type

    try:
        os.remove("database.conf")
    except Exception as e:
        logger.error(f'{e}')
    cur_env = str(os.environ['FLASK_ENV'])
    return flask_app, api, login_manager, cur_env
