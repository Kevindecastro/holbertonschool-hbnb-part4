from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
})

# Route pour récupérer tous les utilisateurs
@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    @api.response(404, 'No users found')
    def get(self):
        """Retrieve a list of all users"""
        users = User.query.all()
        if not users:
            return {'error': 'No users found'}, 404
        return [user.to_dict() for user in users], 200

    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new user"""
        try:
            user_data = request.get_json()

            # Check for required fields
            required_fields = ["first_name", "last_name", "email", "password"]
            if not all(field in user_data for field in required_fields):
                missing_fields = [field for field in required_fields if field not in user_data]
                return {'error': f'Missing required fields: {", ".join(missing_fields)}'}, 400

            # Check if email already exists
            if User.query.filter_by(email=user_data["email"]).first():
                return {'error': 'Email already exists'}, 400

            # Create new user
            new_user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
                password=bcrypt.generate_password_hash(user_data["password"]).decode('utf-8'),
            )

            db.session.add(new_user)
            db.session.commit()

            return new_user.to_dict(), 201

        except IntegrityError:
            db.session.rollback()
            return {'error': 'Database integrity error. The email might already exist.'}, 400
        except Exception as e:
            return {'error': f"An error occurred while creating the user: {str(e)}"}, 500

# Route pour gérer les utilisateurs par ID
@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(404, 'User not found')
    @api.response(200, 'User details retrieved successfully')
    @jwt_required()  # Protect this endpoint
    def get(self, user_id):
        """Retrieve user details by ID"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        if current_user_id != user_id:
            return {'error': 'You can only access your own details'}, 403  # Optionally, you can add authorization checks

        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model)
    @api.response(200, 'User details updated successfully')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user by ID"""
        user_data = request.get_json()
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        if 'password' in user_data:
            user.password = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')

        db.session.commit()
        return user.to_dict(), 200

# Route pour gérer la connexion et créer un JWT
@api.route('/login')
class UserLogin(Resource):
    @api.expect(user_model)
    @api.response(200, 'Login successful')
    @api.response(400, 'Invalid credentials')
    def post(self):
        """Login and generate JWT token"""
        user_data = request.get_json()

        email = user_data.get("email")
        password = user_data.get("password")

        # Find the user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            return {'error': 'Invalid email or password'}, 400

        # Check if the password is correct
        if not bcrypt.check_password_hash(user.password, password):
            return {'error': 'Invalid email or password'}, 400

        # Create JWT token
        access_token = create_access_token(identity=user.id)

        return {'access_token': access_token}, 200
    
# Route pour une ressource protégée, accessible uniquement aux utilisateurs authentifiés
@api.route('/protected', methods=['GET'])
class ProtectedResource(Resource):
    @jwt_required()  # Protection avec JWT
    def get(self):
        """A protected endpoint that only authenticated users can access."""
        current_user_id = get_jwt_identity()  # Récupère l'ID de l'utilisateur authentifié
        user = User.query.get(current_user_id)
        return jsonify(logged_in_as=user.email), 200

# Route admin pour les utilisateurs authentifiés avec JWT
@api.route('/admin')
class AdminResource(Resource):
    @jwt_required()  # Protection avec JWT
    def get(self):
        """Admin-only resource"""
        current_user_id = get_jwt_identity()  
        user = User.query.get(current_user_id)

        if not user:
            return {'error': 'User not found'}, 404

        # Vérification si l'utilisateur est un administrateur
        if not user.is_admin:
            return {'error': 'You do not have permission to access this resource'}, 403  # L'utilisateur n'a pas les droits

        return jsonify({'message': 'Welcome, admin!'}), 200