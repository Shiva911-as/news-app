import requests
import time

# ========================
# Step 1: User Interests
# ========================
user_interests = input("Enter your favorite topics (comma separated): ")
user_profile = {topic.strip().lower(): 1 for topic in user_interests.split(",")}

print("\nYour initial interests:", list(user_profile.keys()), "\n")

# ========================
# Step 2: Related Topics + Synonyms
# ========================
related_topics = {
    "ai": ["artificial intelligence", "machine learning", "deep learning", "nlp"],
    "cricket": ["sports", "football", "ipl", "match"],
    "tech": ["gadgets", "innovation", "startups", "technology"],
    "finance": ["stocks", "economy", "investment", "market"],
    "politics": ["government", "elections", "policy", "parliament"],
}

# Add related topics to profile if not present
for rels in related_topics.values():
    for rel in rels:
        if rel not in user_profile:
            user_profile[rel] = 0.5  # small initial weight

# ========================
# Step 3: Fetch News
# ========================
API_KEY = "afb4ce6d6ca347ebad67c93a75780711"  # replace with your key
# Use broader categories to ensure we get articles
URL = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=50&apiKey={API_KEY}"


def fetch_articles(url, retries=3, delay=5):
    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code == 429:
            print("API rate limit exceeded. Waiting before retrying...")
            time.sleep(delay)
            continue
        try:
            data = response.json()
        except Exception:
            print("Error decoding response. Try again later.")
            return []
        if 'articles' in data:
            return data['articles']
        else:
            print("No articles found. Response:", data)
            return []
    print("Failed to fetch articles after retries.")
    return []


articles_list = fetch_articles(URL)

if not articles_list:
    print("Error fetching news. Check API key, connection, or API limits.")
    exit()

# ========================
# Step 4: Score Articles
# ========================
recommended_articles = []

for article in articles_list:
    title = (article['title'] or "").lower()
    description = (article['description'] or "").lower()
    
    score = 0
    for topic, weight in user_profile.items():
        if topic in title or topic in description:
            score += weight
    
    if score > 0:
        recommended_articles.append((score, article))

# ========================
# Step 5: Display Top 5
# ========================
if recommended_articles:
    recommended_articles.sort(reverse=True, key=lambda x: x[0])
    print("Top Personalized News Headlines:\n")
    for i, (score, article) in enumerate(recommended_articles[:5], start=1):
        print(f"{i}. {article['title']} (Score: {score})")
        # Simulate reading the article: update profile
        read_text = (article['title'] + " " + (article['description'] or "")).lower()
        for topic, rels in related_topics.items():
            if topic in read_text:
                for rel in rels:
                    user_profile[rel] += 0.5  # learn from reading
else:
    print("No personalized news found. Try broader topics or popular ones like 'tech', 'sports'.")
