from flask import Flask
from pymongo import MongoClient
from flask.ext.login import LoginManager
from flask.ext.bower import Bower
from flask.ext.bootstrap import Bootstrap

mongo = MongoClient()
db = mongo.test

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.index'

bower = Bower()
bootstrap = Bootstrap()

def create_app():
    # app = Flask('scheduler')
    app = Flask(__name__)

    app.config.from_object('config')

    login_manager.init_app(app)
    bower.init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .glp import glp as glp_blueprint
    app.register_blueprint(glp_blueprint)


    return app

