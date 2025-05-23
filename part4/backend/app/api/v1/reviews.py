from flask import request
from flask_restx import Namespace, Resource, fields, abort
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Modèles
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})


@api.route('/places/<string:place_id>/reviews')
class PlaceReviews(Resource):
    @api.response(200, 'Reviews retrieved successfully')
    def get(self, place_id):
        """Get all reviews for a place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except Exception as e:
            return {"error": str(e)}, 500

            return [{
                'id': str(review.id),
                'text': review.text,
                'rating': review.rating,
                'user_name': f"{review.user.first_name} {review.user.last_name}",
                'created_at': review.created_at.isoformat()
            } for review in reviews], 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review created successfully')
    def post(self, place_id):
        """Create a new review for a place"""
        current_user = get_jwt_identity()
        review_data = api.payload
        review_data['user_id'] = current_user
        review_data['place_id'] = place_id

        review = facade.create_review(review_data)
        return {
            'id': str(review.id),
            'text': review.text,
            'rating': review.rating,
            'user_name': f"{review.user.first_name} {review.user.last_name}",
            'created_at': review.created_at.isoformat()
        }, 201


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = request.get_json()

        # Validation des données
        if not all(key in review_data for key in ['text', 'rating', 'user_id', 'place_id']):
            return {'error': 'Missing required fields'}, 400

        if not isinstance(review_data['rating'], int) or review_data['rating'] < 1 or review_data['rating'] > 5:
            return {'error': 'Rating must be an integer between 1 and 5'}, 400

        # Création de l'avis via la façade
        review = facade.create_review(review_data)
        if not review:
            return {'error': 'Failed to create review'}, 500

        return review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @jwt_required()
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @jwt_required()
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = request.get_json()

        if 'rating' in review_data and (not isinstance(review_data['rating'], int) or review_data['rating'] < 1 or review_data['rating'] > 5):
            return {'error': 'Rating must be an integer between 1 and 5'}, 400

        updated_review = facade.update_review(review_id, review_data)
        if not updated_review:
            return {'error': 'Review not found'}, 404

        return updated_review.to_dict(), 200
