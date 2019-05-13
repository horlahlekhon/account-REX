import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    user="postgres"
    db = "account_rex"
    pw = "postgres"

    db_url = "127.0.0.1:5432"
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=user, pw=pw, url=db_url, db=db)


class TestConfigs(BaseConfig):
    DEBUG = False
    user="postgres"
    db = "account_rex_test"
    pw = "postgres"

    db_url = "127.0.0.1:5432"
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=user, pw=pw, url=db_url, db=db)
