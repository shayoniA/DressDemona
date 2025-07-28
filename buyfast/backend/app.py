from flask import Flask
from routes.auth import auth
from routes.user import user
from routes.image import image
from routes.feed import feed
from routes.upvote import upvote
from flask_cors import CORS
from flask import send_from_directory
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(image, url_prefix="/image")
app.register_blueprint(feed, url_prefix="/feed")
app.register_blueprint(upvote, url_prefix="/upvote")

@app.route('/uploads/<filename>')
def serve_uploaded_image(filename):
    uploads_dir = os.path.join(os.getcwd(), "uploads")
    return send_from_directory(uploads_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
