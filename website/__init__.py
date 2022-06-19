from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from .database import mongo_db

def create_app(url):
    app = Flask(__name__) #initialization
    app.config['SECRET_KEY'] = 'ddsdwndsuixnuinwd'
    app.config["MONGO_URI"] = url

    from .home_view import home_view
    from .pages import pages
    app.register_blueprint(home_view, url_prefix = '/')
    app.register_blueprint(pages, url_prefix = '/')

    mongo_db.init_app(app)
    return app