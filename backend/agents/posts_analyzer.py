from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_posts(posts):
    prompt = (
        "You will receive a list of clothing descriptions uploaded by a user. "
        "Summarize the user's fashion preferences into 3 short phrases (each max 8 words). "
        "Example output: Floral dresses above knee, V-neck crop tops, Modern bodycon dresses above knee.\n\n"
        f"Descriptions: {posts}\n\n"
        "Do not give any additional information or explanation, just give the 3 phrases separated by comma(,)"
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    text = response.text.strip()
    return [x.strip() for x in text.split(",")]