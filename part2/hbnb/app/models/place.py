import uuid


class Place:
    def __init__(self, title, description, price, latitude, longitude, owner):
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")
        if not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be a number between -90 and 90")
        if not isinstance(longitude, (int, float)) or not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be a number between -180 and 180")

        self.id = str(uuid.uuid4())  # Génère un identifiant unique
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # L'owner pourrait être une autre classe ou un objet avec des attributs comme id, nom
        self.amenities = []

    def add_amenity(self, amenity):
        """Ajoute une commodité à l'endroit"""
        self.amenities.append(amenity)

    def update(self, data):
        """Met à jour les attributs de l'objet en fonction du dictionnaire donné"""
        for key, value in data.items():
            if hasattr(self, key):  # Vérifie si l'attribut existe dans l'objet
                setattr(self, key, value)
        self.save()  # Met à jour le timestamp `updated_at` si tu souhaites gérer une base de données

    def save(self):
        """Méthode pour mettre à jour l'objet (optionnel si tu veux gérer une base de données plus tard)"""
        # Ajoute ici la logique pour persister l'objet
        print(f"Place {self.id} saved to database.")  # Exemple de message

    def __str__(self):
        return f"Place {self.title}, {self.price} per night"

