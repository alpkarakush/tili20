from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from flask_moment import Moment
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)



admin = Admin(app, name='Tili', template_mode='bootstrap3')
login = LoginManager(app)

# logging.basicConfig(filename='main.log', level=logging.DEBUG)
# app.logger.setLevel(logging.DEBUG)
# app.logger.info('Tili')

moment = Moment(app)

from app import routes, models
migrate = Migrate(app, db)
from app.models import User, Definition, Word
from app.admin_views import AdminView

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Definition, db.session))
admin.add_view(AdminView(Word, db.session))