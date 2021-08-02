from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
from app.config import Config


# PyMongo instantiation
mongo = PyMongo()
# Flask email instantiation
mail = Mail()


def create_app(default_config=Config):
    """
    Configure the application instances
    Import and register blueprints for separation of concerns
    """
    app = Flask(__name__)
    # Configure the application instance using the Config class
    app.config.from_object(default_config)
    # setup an instance of PyMongo
    mongo.init_app(app)
    # set up an instance of Flask mail
    mail.init_app(app)

    # Import and register Blueprints
    from app.main import main
    from app.auth import auth
    from app.users import users
    from app.groups import groups
    from app.validators.validators import validators

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(groups)
    app.register_blueprint(validators)

    return app
