from flask import Flask, request, jsonify
from applications.database import db
from applications.models import User
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    if not data['email']:
        return jsonify({"message": "Email is required"}), 400
    
    if not data['username']:
        return jsonify({"message": "Username is required"}), 400
    
    if not data['password']:
        return jsonify({"message": "Password is required"}), 400
    
    if not data['confirm_password']:
        return jsonify({"message": "Confirm Password is required"}), 400
    
    if data['password'] != data['confirm_password']:
        return jsonify({"message": "Passwords do not match"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 400
    
    new_user = User(
        username=data['username'],
        name=data['name'] if 'name' in data else "",
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    if not data['email']:
        return jsonify({"message": "Email is required"}), 400

    if not data['password']:
        return jsonify({"message": "Password is required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"message": "Invalid email or password"}), 401

    additional_claims = {"is_admin": user.is_admin}

    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 200
