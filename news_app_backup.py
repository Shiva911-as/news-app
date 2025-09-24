import requests

# 🔑 Your NewsAPI key
api_key = "afb4ce6d6ca347ebad67c93a75780711"

# URL to fetch top headlines (you can change 'q' to any topic like 'technology', 'sports', etc.)
url = f"https://newsapi.org/v2/everything?q=technology&sortBy=publishedAt&apiKey={api_key}"

try:
    response = requests.get(url)
    response.raise_for_status()  # Will raise an HTTPError if the request failed
    data = response.json()

    if 'articles' in data:
        print("\nTop 5 News Headlines:\n")
        for i, article in enumerate(data['articles'][:5], start=1):
            print(f"{i}. {article['title']}")
    else:
        print("No articles found. Response:", data)

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")
