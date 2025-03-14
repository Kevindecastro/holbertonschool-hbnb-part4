from uuid import uuid4

class Amenity:
    def __init__(self, name):
        self.name = name

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner, amenities=None):
        self.id = str(uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = amenities or []  # Liste d'objets Amenity

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be an instance of Amenity")
        self.amenities.append(amenity)

    def to_dict(self):
        """Convertir l'objet Place en dictionnaire"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner,
            'reviews': [review.to_dict() for review in self.reviews],
            'amenities': [a.name for a in self.amenities]  # Supposons que `a` est un objet Amenity
        }