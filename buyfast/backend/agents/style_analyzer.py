import ollama
def analyze_style(posts):
    prompt = (
        "You will receive a list of clothing descriptions uploaded by a user. Summarize the user's fashion preferences in about 40 words. Here are the descriptions of the user's clothes: \n"
        f"Descriptions: {posts}\n"
    )
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    desc = response['message']['content'].strip()
    return desc
