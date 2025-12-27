from flask import Blueprint, request, jsonify
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if db.users.find_one({"email": data['email']}):
        return jsonify({"msg": "Email already exists"}), 409
    hashed_password = generate_password_hash(data['password'])
    user = {
        "email": data['email'],
        "password": hashed_password,
        "linked_sites": data['linked_sites'],
        "my_style": "",
        "posts": [],
        "post_images": [],
        "post_upvotes": [],
        "choices": [],
        "likes": []
    }
    db.users.insert_one(user)
    return jsonify({"msg": "User created"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = db.users.find_one({"email": data['email']})
    if user and check_password_hash(user['password'], data['password']):
        return jsonify({"msg": "Login successful", "user_id": str(user['_id'])})
    return jsonify({"msg": "Invalid credentials"}), 401
