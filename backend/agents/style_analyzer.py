from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_style(posts):
    prompt = (
        "You will receive a list of clothing descriptions uploaded by a user. Summarize the user's fashion preferences in about 40 words. Here are the descriptions of the user's clothes: \n"
        f"Descriptions: {posts}\n"
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    # text = response.text.strip()
    # return [x.strip() for x in text.split(",")]
    return response.text.strip()