import os

from  flask_bcrypt import Bcrypt
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from project.app.config  import *
import logging 

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

bcrypt = Bcrypt(app)
database = SQLAlchemy(app)


loglevels = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG
}
logger = logging.getLogger(__name__)
formatter = logging.Formatter('{asctime}s {levelname}s {message}s' )
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.DEBUG)


