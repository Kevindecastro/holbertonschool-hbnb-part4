from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('admin', description='Endpoints réservés aux administrateurs')

@api.route('/')
class AdminResource(Resource):
    @api.doc(security='Bearer Auth')  # Indique que cet endpoint est protégé
    @jwt_required()  # Protège l'endpoint avec JWT
    def get(self):
        """Un endpoint réservé aux administrateurs"""
        current_user_id = get_jwt_identity()  
        claims = get_jwt()

        # Vérifie si l'utilisateur est un administrateur
        if not claims.get('is_admin'):
            return {'error': 'Accès refusé. Réservé aux administrateurs.'}, 403

        return {'message': f'Bienvenue, administrateur {current_user_id}'}, 200