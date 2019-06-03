import os
import click

basedir = os.path.abspath(os.path.dirname("../../"))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key_')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    RSA_PUBLIC_KEY= os.path.join(basedir, 'keys/private')
    RSA_PRIVATE_KEY=os.path.join(basedir, 'keys/public.pub')
    SERVER_NAME = "localhost:5000"
    DEBUG = True
    user="postgres"
    db = "account_rex"
    pw = "postgres"
    db_url = "127.0.0.1:5432"
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=user, pw=pw, url=db_url, db=db)


class TestingConfig(BaseConfig):
    RSA_PUBLIC_KEY= os.path.join(basedir, 'keys/private')
    RSA_PRIVATE_KEY=os.path.join(basedir, 'keys/public.pub')
    DEBUG = True
    user="postgres"
    db = "account_rex_test"
    pw = "postgres"

    db_url = "127.0.0.1:5432"
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=user, pw=pw, url=db_url, db=db)
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(BaseConfig):
    DEBUG = False

