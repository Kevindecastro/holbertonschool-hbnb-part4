from flask_restx import Namespace, Resource, fields, abort
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Modèles
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


def format_place(place_obj):
    """ Helper function to format place data """
    return {
        "id": place_obj.id,
        "title": place_obj.title,
        "description": place_obj.description,
        "price": place_obj.price,
        "latitude": place_obj.latitude,
        "longitude": place_obj.longitude,
        "owner_id": place_obj.owner.id,
        "amenities": [a.name for a in place_obj.amenities]
    }


@api.route('/')
class PlaceList(Resource):
    @jwt_required() 
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """ Register a new place """
        place_data = api.payload
        place_obj = facade.create_place(place_data)
        return format_place(place_obj), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """ Retrieve all places """
        places = facade.get_all_places()
        return [format_place(p) for p in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @jwt_required() 
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """ Retrieve a place's details by ID, including owner and amenities """
        place_obj = facade.get_place(place_id)
        if not place_obj:
            abort(404, message="Place not found")
        return format_place(place_obj), 200

    @api.expect(place_model)
    @jwt_required() 
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """ Update a place's information """
        current_user = get_jwt_identity()

        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        
        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        # Vérifier si l'utilisateur est le propriétaire du lieu
        if place.owner != current_user:
            return {'error': 'Unauthorized action'}, 403

        # Mettre à jour les attributs du lieu
        data = api.payload
        for key, value in data.items():
            setattr(place, key, value)

        # Mettre à jour le lieu dans le repository
        facade.update_place(place)
        return format_place(place), 200

