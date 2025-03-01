from datetime import datetime
from math import e
import uuid
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import InMemoryRepository
from flask import jsonify, request


class HBnBFacade:
    def __init__(self):
        # Dépôts en mémoire pour chaque entité
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # --- Opérations sur les utilisateurs --- #
    def create_user(self, user_data):
        """Créer un nouvel utilisateur"""
        user = User(**user_data)
        self.user_repo.add(user)  
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def update_user(self, user_id, user_data):
        """Met à jour les informations de l'utilisateur"""
        user = self.user_repo.get(user_id)
        if not user:
            return None
    
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']
    
        self.user_repo.update(user)
    
        return user

    # --- Opérations sur les amenities --- #
    def create_amenity(self, amenity_data):
        """Créer une nouvelle amenity"""
        try:
            amenity = Amenity(**amenity_data)  # Utiliser la classe Amenity
            self.amenity_repo.add(amenity)  # Ajouter l'amenity au dépôt
            return amenity
        except Exception as e:
            return {'error': f"An error occurred while creating the amenity: {str(e)}"}, 500

    def get_all_amenities(self):
        """Retourne toutes les amenities"""
        try:
            return self.amenity_repo.get_all()
        except Exception as e:
            return {'error': f"An error occurred while fetching amenities: {str(e)}"}, 500

    def get_amenity(self, amenity_id):
        """Retourne une amenity par ID"""
        try:
            return self.amenity_repo.get(amenity_id)
        except Exception as e:
            return {'error': f"An error occurred while fetching the amenity: {str(e)}"}, 500

    def get_amenity_by_name(self, name):
        """Retourne une amenity par nom"""
        try:
            return self.amenity_repo.get_by_attribute('name', name)
        except Exception as e:
            return {'error': f"An error occurred while fetching amenity by name: {str(e)}"}, 500

    def update_amenity(self, amenity_id, amenity_data):
        """Met à jour une amenity par ID"""
        try:
            if not amenity_data:
                return {'error': 'No data provided'}, 400

            amenity = self.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404

            # Mise à jour des données de l'amenity
            for key, value in amenity_data.items():
                setattr(amenity, key, value)

            # Retourner l'amenity mis à jour sous forme de dictionnaire
            return amenity.to_dict()

        except Exception as e:
            return {'error': f"An error occurred while updating the amenity: {str(e)}"}, 500

    # --- Opérations sur les lieux --- #
    def create_place(self, place_data):
        if place_data["price"] < 0:
            raise ValueError("Price must be a non-negative value.")
        if not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found.")

        place_obj = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )
        place_obj.amenities = [] if not hasattr(place_obj, "amenities") else place_obj.amenities

        if "amenities" in place_data:
            amenities = []
            for amenity_id in place_data["amenities"]:
                amenity_obj = self.amenity_repo.get(amenity_id)
                if amenity_obj:
                    amenities.append(amenity_obj)
            place_obj.amenities = amenities

        self.place_repo.add(place_obj)
        return place_obj

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        if "price" in data and data["price"] < 0:
            raise ValueError("Price must be a non-negative value.")
        if "latitude" in data and not (-90 <= data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if "longitude" in data and not (-180 <= data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        if "owner_id" in data:
            new_owner = self.user_repo.get(data["owner_id"])
            if not new_owner:
                raise ValueError("Owner not found.")
        place.owner = new_owner
        data.pop("owner_id")

        if "amenities" in data:
            new_amenities = []
            for amenity_id in data["amenities"]:
                amenity_obj = self.amenity_repo.get(amenity_id)
                if amenity_obj:
                    new_amenities.append(amenity_obj)
            place.amenities = new_amenities
            data.pop("amenities")

        place.update(data)
        self.place_repo.add(place)
        return place 

    # --- Opérations sur les review --- #
    def create_review(self, review_data):
            """Create a new review"""
            review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                user_id=review_data['user_id'],
                place_id=review_data['place_id']
            )
            self.review_repo.add(review)
            return review

    def get_all_reviews(self):
            """Retrieve all reviews"""
            return self.review_repo.get_all()

    def get_review(self, review_id):
            """Retrieve a review by ID"""
            return self.review_repo.get(review_id)

    def update_review(self, review_id, review_data):
            """Update a review by ID"""
            review = self.review_repo.get(review_id)
            if not review:
                return None
            for key, value in review_data.items():
                if hasattr(review, key):
                    setattr(review, key, value)
            review.updated_at = datetime.utcnow()
            self.review_repo.update(review)
            return review

    def delete_review(self, review_id):
            """Delete a review by ID"""
            return self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
            """Retrieve all reviews for a specific place"""
            return [review for review in self.review_repo.get_all() if review.place_id == place_id]