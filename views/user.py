from flask import jsonify, request, Blueprint
from flask_bcrypt import Bcrypt
from models import db, User


user_bp = Blueprint('user_bp', __name__)

#user
@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data['username']
    email = data['email']
    hashed_password = Bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

#update
@user_bp.route('/user', methods=['PUT'])
def update_user():
    data = request.json
    id = data['id']
    username = data['username']
    email = data['email']
    hashed_password = Bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User.query.get(id)
    if user:
        user.username = username
        user.email = email
        user.password = hashed_password
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

#delete
@user_bp.route('/user', methods=['DELETE'])
def delete_user():
    id = request.json['id']
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 401

#login
@user_bp.route('/user/login', methods=['POST'])
def login_user():
    data = request.json
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user and Bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

#logout
@user_bp.route('/user/logout', methods=['POST'])
def logout_user():
    return jsonify({'message': 'Logout successful'}), 200
