# app/models.py

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email, password=None, _id=None):
        self.username = username
        self.email = email
        if password:
            # Specify a supported hashing method
            self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        else:
            self.password_hash = None
        self.id = _id

    @staticmethod
    def find_by_email(email):
        user_data = current_app.db.users.find_one({'email': email})
        if user_data:
            return User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data.get('password_hash'),
                _id=user_data['_id']
            )
        return None

    @staticmethod
    def find_by_username(username):
        user_data = current_app.db.users.find_one({'username': username})
        if user_data:
            return User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data.get('password_hash'),
                _id=user_data['_id']
            )
        return None

    def save_to_db(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash
        }
        result = current_app.db.users.insert_one(user_data)
        self.id = result.inserted_id

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
