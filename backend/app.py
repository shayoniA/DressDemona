from flask import Flask
from routes.auth import auth
from routes.user import user
from routes.image import image
from routes.feed import feed
from routes.upvote import upvote
from flask_cors import CORS
from flask import send_from_directory
import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "frontend"),
    static_url_path=""
)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(image, url_prefix="/image")
app.register_blueprint(feed, url_prefix="/feed")
app.register_blueprint(upvote, url_prefix="/upvote")

@app.route("/")
def index():
    return app.send_static_file("login.html")

@app.route('/uploads/<path:filename>')
def serve_uploaded_image(filename):
    uploads_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    return send_from_directory(uploads_dir, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)