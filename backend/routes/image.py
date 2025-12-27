import os
from flask import Blueprint, request, jsonify
from database import db
from agents.image_analyzer import describe_image_ollama
from agents.style_analyzer import analyze_style
from utils.clustering import update_user_clusters
from bson import ObjectId

image = Blueprint('image', __name__)
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads"))

@image.route('/upload/<user_id>', methods=['POST'])
def upload(user_id):
    print("Entered into the backend successfully!")
    if 'images' not in request.files:
        return jsonify({"error": "No files part in request"}), 400
    files = request.files.getlist('images')
    if not files:
        return jsonify({"error": "No images uploaded"}), 400
    responses = []
    user_folder = os.path.join(UPLOAD_FOLDER, user_id)
    os.makedirs(user_folder, exist_ok=True)
    print("Now it begins...")

    for file in files:
        if file.filename == '':
            continue
        filepath = os.path.join(user_folder, file.filename)
        file.save(filepath)
        try:
            print("Describing image:", filepath)
            description = describe_image_ollama(filepath)
        except Exception as e:
            print("Image analysis failed:", e)
            description = "Could not analyze image."
        print("Updating ting ting...")
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {
                    "posts": description,
                    "post_images": filepath,
                    "post_upvotes": 0
            }}
        )
        responses.append(description)
    
    print("Analyzing updated user style...")
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user and "posts" in user:
        all_posts = user["posts"]
        try:
            my_style_summary = analyze_style(all_posts)
        except Exception as e:
            print("Style analysis failed:", e)
            my_style_summary = "Style summary unavailable."

        print("Updating user's my_style field...")
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"my_style": my_style_summary}}
        )

        # Save into user_clusters
        db.user_clusters.update_one(
            {"user_id": user_id},
            {"$set": {"style": my_style_summary}},
            upsert=True
        )
        update_user_clusters()

    print("Returning response:", responses)
    return jsonify(descriptions=responses), 200
