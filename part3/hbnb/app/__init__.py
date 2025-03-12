from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


# Initialize instances
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


# Import namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.ameneties import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns

import logging
from logging import FileHandler, WARNING

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    # Configure logging
    if not app.debug:
        from logging import FileHandler, WARNING
        file_handler = FileHandler('errorlog.log')
        file_handler.setLevel(WARNING)
        app.logger.addHandler(file_handler)

    # Register namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.ameneties import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    

    from flask_restx import Api
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app