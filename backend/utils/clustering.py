from database import db
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

def update_user_clusters():
    # Fetch all users with 'my_style' description
    users = list(db.users.find({"my_style": {"$exists": True}}))
    if not users:
        return

    styles = [user["my_style"] for user in users]
    user_ids = [str(user["_id"]) for user in users]

    # Convert styles to embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(styles)

    # Decide number of clusters
    num_clusters = 2
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    # Save cluster assignments in user_clusters collection
    for user_id, style, label in zip(user_ids, styles, labels):
        db.user_clusters.update_one(
            {"user_id": user_id},
            {"$set": {"style": style, "cluster": int(label)}},
            upsert=True
        )
