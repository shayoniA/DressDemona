from flask import Blueprint, request, jsonify
from database import db
from bson import ObjectId
from agents.posts_analyzer import summarize_posts
from agents.recommendor import fetch_from_linked_sites

user = Blueprint("user", __name__)

@user.route("/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    user["_id"] = str(user["_id"])
    return jsonify({
        "email": user.get("email", ""),
        "linked_sites": user.get("linked_sites", []),
        "my_style": user.get("my_style", ""),
        "posts": user.get("posts", []),
        "post_images": user.get("post_images", []),
        "post_upvotes": user.get("post_upvotes", []),
        "choices": user.get("posts", []),
        "likes": user.get("likes", [])
    })

@user.route('/recommendations/<user_id>', methods=['POST'])
def get_recommendations(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    posts = user.get("posts", [])
    if not posts or len(posts) == 0:
        return jsonify(recommendations=[]), 200

    choices = summarize_posts(posts)
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"choices": choices}})

    # Get recommendations from linked sites
    linked_sites = user.get("linked_sites", [])
    recommendations = fetch_from_linked_sites(choices, linked_sites)

    return jsonify(recommendations=recommendations), 200
