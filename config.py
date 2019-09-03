class BaseConfig:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = int(port)
        self.DATABASE_CONNECTION_URI =\
            f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'


class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """
    host = 'localhost' # in case of using docker
    FLASK_DEBUG = 1
    DEBUG = True
    # SQLALCHEMY_ECHO = True


class ProductionConfig(BaseConfig):
    """
    Production configurations
    """
    FLASK_DEBUG = 0


class DockerConfig(BaseConfig):
    """
    Production configurations
    """
    host = 'database'
    SQLALCHEMY_ECHO = True
    FLASK_DEBUG = 1
