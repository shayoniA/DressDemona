from flask import Blueprint, jsonify, request
from agents.image_analyzer import describe_image_ollama
from database import db
from bson import ObjectId

upvote = Blueprint('upvote', __name__)

@upvote.route('/<user_id>/<int:post_index>', methods=['POST'])
def upvote_post(user_id, post_index):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if post_index >= len(user.get("post_upvotes", [])):
        return jsonify({"error": "Invalid post index"}), 400
    
    # Get upvoter ID
    upvoter_id = request.args.get("upvoter_id")
    if not upvoter_id:
        return jsonify({"error": "Missing upvoter_id"}), 400

    upvoter = db.users.find_one({"_id": ObjectId(upvoter_id)})
    if not upvoter:
        return jsonify({"error": "Upvoter not found"}), 404

    # Prevent multiple upvotes
    image_path = user.get("post_images", [])[post_index]
    if image_path in upvoter.get("likes", []):
        return jsonify({"error": "Already upvoted this post"}), 400

    # Increment upvote
    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {f"post_upvotes.{post_index}": 1}}
    )

    try:
        description = describe_image_ollama(image_path)
    except Exception as e:
        return jsonify({"error": f"Failed to describe image: {str(e)}"}), 500

    # Append to upvoter's likes and posts
    db.users.update_one(
        {"_id": ObjectId(upvoter_id)},
        {
            "$addToSet": {
                "likes": image_path,
                "posts": description
            }
        }
    )

    print("Backend upvote done!")
    return jsonify({"message": "Upvoted successfully"}), 200
