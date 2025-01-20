from flask import jsonify, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

user_bp = Blueprint('user_bp', __name__)

# Create a new user
@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.json
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Invalid input, all fields are required'}), 400

    username = data['username']
    email = data['email']
    hashed_password = generate_password_hash(data['password'])

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 409

    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Update current user
@user_bp.route('/user', methods=['PATCH'])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()  # Get user ID from JWT
    user = User.query.get(current_user_id)  # Fetch the current user
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already in use'}), 409
        user.email = data['email']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

# Delete current user
@user_bp.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    current_user_id = get_jwt_identity()  # Get the user ID from JWT
    user = User.query.get(current_user_id)  # Fetch the current user
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# Login user
@user_bp.route('/user/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid email or password'}), 401

# Logout user
@user_bp.route('/user/logout', methods=['POST'])
@jwt_required()
def logout_user():
    return jsonify({'message': 'Logout successful'}), 200
