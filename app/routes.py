# app/routes.py

from flask import Blueprint, jsonify, current_app
from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return 'Backend is running!', 200

@main.route('/test_db', methods=['GET'])
def test_db():
    try:
        # Insert a test user
        test_user = User(username='testuser', email='test@example.com', password='password')
        test_user.save_to_db()

        # Retrieve users from the database
        users_cursor = current_app.db.users.find()
        user_list = [{'username': user['username'], 'email': user['email']} for user in users_cursor]

        return jsonify({'users': user_list}), 200
    except Exception as e:
        import traceback
        traceback_str = ''.join(traceback.format_exception(None, e, e.__traceback__))
        return jsonify({'error': traceback_str}), 500
