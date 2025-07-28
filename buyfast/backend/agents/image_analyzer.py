from PIL import Image
import ollama
import base64

def describe_image_ollama(img_path):
    print(f"This is the path ------ {img_path}")
    try:
        with open(img_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        prompt = "Describe the clothing in this image in less than 8 words. The description should contain dress-length, type, etc., but should not contain not dress-color."

        response = ollama.chat(
            model="llava",
            messages=[{
                "role": "user",
                "content": prompt,
                "images": [image_base64]
            }]
        )
        print("Response from ollama:", response)
        return response['message']['content']
    
    except Exception as e:
        print("Error in describe_image_ollama:", e)
        raise e
