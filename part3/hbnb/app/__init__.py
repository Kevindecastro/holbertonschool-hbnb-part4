from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.ameneties import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_ns
from app.extensions import bcrypt
from app.extensions import jwt
from config import Config

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'votre_cle_secrete_jwt'
    app.config.from_object(config_class)
    app.config.from_object(Config)
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Utilisez "Bearer <token>" pour vous authentifier.'
    }
}
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', authorizations=authorizations, security='Bearer Auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    return app
