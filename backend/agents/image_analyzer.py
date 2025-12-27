from PIL import Image
import base64
from dotenv import load_dotenv
load_dotenv()
import os
import json
import re
from google import genai
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def describe_image_ollama(img_path):
    print(f"This is the path ------ {img_path}")
    try:
        image = Image.open(img_path)
        prompt = "Describe the clothing in this image in less than 8 words. The description should contain dress-length, type, etc., but should not contain not dress-color."
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                image
            ]
        )
        print("Response from Gemini:", response.text)
        return response.text
    
    except Exception as e:
        print("Error in describe_image_ollama:", e)
        raise e