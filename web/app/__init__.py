from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from flask_moment import Moment


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

app.logger.setLevel(logging.INFO)
app.logger.info('Tili')

moment = Moment(app)

from app import routes, models