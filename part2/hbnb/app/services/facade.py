from app.models.user import User
from app.models.place import Place
from app.persistence.repository import InMemoryRepository
from flask import request

class HBnBFacade:
    def __init__(self):
        # Dépôts en mémoire pour chaque entité
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        # D'autres dépôts pour Review, Amenity peuvent être ajoutés plus tard

    # --- Opérations sur les utilisateurs ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_all_users(self):
        try:
            return self.user_repo.get_all()
        except Exception as e:
            return {'error': f"An error occurred while fetching users: {str(e)}"}, 500

    def get_user(self, user_id):
        try:
            return self.user_repo.get(user_id)
        except Exception as e:
            return {'error': f"An error occurred while fetching the user: {str(e)}"}, 500

    def get_user_by_email(self, email):
        try:
            return self.user_repo.get_by_attribute('email', email)
        except Exception as e:
            return {'error': f"An error occurred while fetching user by email: {str(e)}"}, 500

    def update_user(self, user_id, user_data):
        """Update user details by ID"""
        try:
            if not user_data:
                return {'error': 'No data provided'}, 400

            user = self.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            # Mise à jour des informations utilisateur
            for key, value in user_data.items():
                setattr(user, key, value)

            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 200

        except Exception as e:
            return {'error': f"An error occurred while updating the user: {str(e)}"}, 500

    # --- Opérations sur les lieux ---
    def create_place(self, place_data):
        """Créer un lieu avec validation des attributs"""
        try:
            price = place_data.get('price')
            latitude = place_data.get('latitude')
            longitude = place_data.get('longitude')

            # Validation des prix, latitude et longitude
            if price is not None and price < 0:
                raise ValueError("Le prix doit être positif ou nul.")
            if latitude is not None and not (-90 <= latitude <= 90):
                raise ValueError("La latitude doit être comprise entre -90 et 90.")
            if longitude is not None and not (-180 <= longitude <= 180):
                raise ValueError("La longitude doit être comprise entre -180 et 180.")

            # Vérification du propriétaire
            owner_id = place_data.get('owner_id')
            owner = self.user_repo.get(owner_id)
            if not owner:
                raise ValueError("Propriétaire non trouvé.")

            # Créer le lieu
            place = Place(
                title=place_data.get('title'),
                description=place_data.get('description', ''),
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner=owner,
                amenities=place_data.get('amenities', [])
            )
            self.place_repo.add(place)
            return place

        except ValueError as ve:
            return {'error': str(ve)}, 400
        except Exception as e:
            return {'error': f"An error occurred while creating the place: {str(e)}"}, 500

    def get_place(self, place_id):
        try:
            return self.place_repo.get(place_id)
        except Exception as e:
            return {'error': f"An error occurred while fetching the place: {str(e)}"}, 500

    def get_all_places(self):
        try:
            return self.place_repo.get_all()
        except Exception as e:
            return {'error': f"An error occurred while fetching places: {str(e)}"}, 500

    def update_place(self, place_id, place_data):
        """Mettre à jour un lieu par ID"""
        try:
            place = self.place_repo.get(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Validation des nouveaux attributs
            if 'price' in place_data and place_data['price'] < 0:
                raise ValueError("Le prix doit être positif ou nul.")
            if 'latitude' in place_data and not (-90 <= place_data['latitude'] <= 90):
                raise ValueError("La latitude doit être comprise entre -90 et 90.")
            if 'longitude' in place_data and not (-180 <= place_data['longitude'] <= 180):
                raise ValueError("La longitude doit être comprise entre -180 et 180.")

            # Mise à jour de l'identifiant du propriétaire si modifié
            if 'owner_id' in place_data:
                owner = self.user_repo.get(place_data['owner_id'])
                if not owner:
                    raise ValueError("Propriétaire non trouvé.")
                place_data['owner'] = owner
                del place_data['owner_id']  # Supprimer l'ID du propriétaire pour éviter un conflit

            # Mise à jour de l'objet place avec les nouvelles données
            for key, value in place_data.items():
                setattr(place, key, value)

            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': place.owner.id,
                'amenities': place.amenities
            }, 200

        except ValueError as ve:
            return {'error': str(ve)}, 400
        except Exception as e:
            return {'error': f"An error occurred while updating the place: {str(e)}"}, 500
