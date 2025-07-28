import ollama
def summarize_posts(posts):
    prompt = (
        "You will receive a list of clothing descriptions uploaded by a user. "
        "Summarize the user's fashion preferences into 3 short phrases (each max 8 words). "
        "Example output: Floral dresses above knee, V-neck crop tops, Modern bodycon dresses above knee.\n\n"
        f"Descriptions: {posts}\n\n"
        "Do not give any additional information or explanation, just give the 3 phrases separated by comma(,)"
    )
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response['message']['content']
    lines = [x.strip() for x in response['message']['content'].split(",")]
    return lines
