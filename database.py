import logging as logger
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from config import (DevelopmentConfig,
                    )
from filters import datetimeformat, file_type
from models import db
from resources import _read_parameters_store
from cloud_watch.logs.log_events import CloudWatchLogger

#  todo move to separate class obj

logger.basicConfig(filename='app_logs',
                            filemode='a',
                            format=f'%(levelname)s:%(message)s',
                            datefmt='%H:%M:%S',
                            level=logger.INFO)

param_store_names = {
    'prod': 'sfigiel-prod-db-cred',
    'dev': 'sfigiel-dev-db-cred',
    'docker': 'sfigiel-docker-db-cred',
}


def _cloud_watch_monitoring():
    log = CloudWatchLogger()
    #  todo check if ParameterStore exists

    if not log.describe_log_groups()['logGroups']:
        log.create_log_group()
        log.create_log_stream()
        log.put_log_events(message='init logs')  # in case of getting new sequenceToken
    else:
        log.put_log_events(message='start app...')
    return log


def create_app():
    cur_env = str(os.environ['FLASK_ENV'])

    cw_log = _cloud_watch_monitoring()

    param_store_name = param_store_names[cur_env]
    param_store = _read_parameters_store(param_store_name, True)
    config = DevelopmentConfig(*param_store)

    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'the random string'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    logger.info(f'DATABASE_CONNECTION_URI: {config.DATABASE_CONNECTION_URI}')
    cw_log.put_log_events(message=f'DATABASE_CONNECTION_URI: {config.DATABASE_CONNECTION_URI}')

    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    logger.info(f'CREATING DB ENGINE ...')
    cw_log.put_log_events(message=f'CREATING DB ENGINE ...')

    engine = create_engine(flask_app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    logger.info(f'DATABASE_ENGINE: {database_exists(engine.url)}')
    cw_log.put_log_events(message=f'DATABASE_ENGINE: {database_exists(engine.url)}')

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

    if os.path.exists("database.conf"):
        os.remove("database.conf")

    return flask_app, api, login_manager, cur_env, cw_log
