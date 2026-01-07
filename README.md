# DressDemona
An AI-powered fashion-discovery platform that helps users define their personal style through outfit uploads and receive curated clothing recommendations across multiple e-commerce platforms. By combining computer vision and LLMs, DressDemona creates a personalized fashion experience. Users can upload outfit images and get recommendations from websites like Zara and Amazon, all tailored to their fashion preferences.

**Demo Video:** [https://drive.google.com/file/d/1PP9bRJ21m0zf_isI5kRoBzH0NZQ6N9OQ/view]

---

## How to Run

### Backend Setup
```
cd backend
python -m venv venv
venv\Scripts\activate    # MacOS/Linux: source venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Create .env file inside backend/:
```
GOOGLE_API_KEY=your_gemini_api_key
MONGO_URI=your_mongodb_connection_string
```

### Run the application:
```
python app.py
```

---

## Key Features

1. **LLM-powered Outfit Understanding** – Upload outfit images and automatically extract concise clothing descriptions using a multimodal LLM.

2. **Personal Style Profiling** – Build a dynamic fashion profile based on uploaded outfits.

3. **Style-Based Social Feed** – Users are clustered based on fashion preferences and shown outfits from similar users.

4. **Cross-Platform Shopping Recommendations** – Fetches fashion items matching the user’s style from multiple shopping sites (here, Amazon and Zara).

5. **End-to-End Full Stack System** – Authentication, image uploads, feed ranking, clustering, and recommendations.

---

## Tech Stack

1. **Frontend** – HTML, CSS, JavaScript (React.js)
2. **Backend** – Python, Flask, Pillow (for image processing)
3. **AI & ML** – Google Gemini API (LLM-powered), SEntence transformers, KMeans Clustering (scikit-learn)
4. **Database** – MongoDB (for users and cluster-labels)
5. **Web Scraping** – Selenium, BeautifulSoup
7. **Deployment** – Render

---

## Why I Built DressDemona

Finding clothes that genuinely match personal style across multiple platforms is time-consuming and fragmented. Most fashion apps rely only on filters or static recommendations. I built DressDemona to explore how AI, computer vision, and user behavior can work together to:

- Understand fashion visually, and learn evolving personal style
- Combine personal styles with web-scraped recommendations from multiple sites using LLMs
- Provide feed containing outfit recommendations of other users who share similar fashion tastes
- Create a more intuitive and human-like fashion discovery experience

---

## Future Improvements
Replace scraping with official e-commerce APIs
Add comment system and follower graph

---

## Author
**Sayani Adhikary**
