from flask import Blueprint, jsonify
from utils.clustering import update_user_clusters
from database import db
from bson import ObjectId

feed = Blueprint('feed', __name__)

@feed.route('/<user_id>', methods=['GET'])
def get_feed(user_id):
    update_user_clusters()
    user_cluster = db.user_clusters.find_one({"user_id": user_id})
    if not user_cluster or "cluster" not in user_cluster:
        return jsonify({"error": "User cluster not found"}), 404

    user_cluster_id = user_cluster["cluster"]
    cluster_users = db.user_clusters.find({"cluster": user_cluster_id, "user_id": {"$ne": user_id}})

    feed_items = []
    for u in cluster_users:
        uid = u["user_id"]
        user = db.users.find_one({"_id": ObjectId(uid)})
        if user:
            for i, (img, upvotes) in enumerate(zip(user.get("post_images", []), user.get("post_upvotes", []))):
                feed_items.append({
                    "user_id": str(user["_id"]),
                    "post_index": i,
                    "image": img,
                    "upvotes": upvotes
                })

    # Sort by upvotes descending
    feed_items.sort(key=lambda x: x["upvotes"], reverse=True)
    return jsonify(feed=feed_items)
