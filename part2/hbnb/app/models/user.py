from app.models.base_model import BaseModel


class User:
    id_counter = 1

    def __init__(self, first_name, last_name, email):
        self.id = User.id_counter
        User.id_counter += 1
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire pour JSON"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
