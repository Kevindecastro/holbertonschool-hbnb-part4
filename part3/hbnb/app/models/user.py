import uuid
from app.extensions import bcrypt
from app.extensions import jwt

class User:
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        self.id = str(uuid.uuid4())  # Génère un UUID unique sous forme de chaîne
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def hash_password(self, password):
        """Hache le mot de passe avant de le stocker."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe fourni correspond au mot de passe haché."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire pour JSON.
        Exclut le mot de passe pour des raisons de sécurité."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }