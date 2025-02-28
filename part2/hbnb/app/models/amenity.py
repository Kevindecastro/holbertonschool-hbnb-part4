class Amenity:
    # Variable de classe pour suivre l'ID global
    _id_counter = 1

    def __init__(self, name, description=None):
        # Utilisation de la variable de classe pour définir l'ID
        self.id = Amenity._id_counter
        Amenity._id_counter += 1  # Incrémenter l'ID pour la prochaine instance
        self.name = name
        self.description = description

    def to_dict(self):
        """Retourner les informations de l'amenity sous forme de dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
