from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from flask_moment import Moment
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_caching import Cache
from logging.handlers import RotatingFileHandler
import os 
from flask_admin import Admin

db = SQLAlchemy()
cache = Cache()
login = LoginManager()
moment = Moment()
migrate = Migrate()
# admin = Admin(name='Tili', template_mode='bootstrap3')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
    admin = Admin(app, name='Tili Admin', template_mode='bootstrap3')
    
    # Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    with app.app_context():
        # Admin
        from app.models import User, Definition, Word
        from app.admin_views import AdminView
        
        admin.add_view(AdminView(User, db.session))
        admin.add_view(AdminView(Definition, db.session))
        admin.add_view(AdminView(Word, db.session))
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    # Log
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/tili.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
    
    
    return app


from app import models
