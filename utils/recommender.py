import requests

def get_books_by_genre(query):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"
        print(f"🔗 Google Books URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        books = response.json().get("items", [])
        print(f"✅ Google Books returned {len(books)} items")

        results = []
        for book in books:
            info = book.get("volumeInfo", {})
            results.append({
                "title": info.get("title", "Unknown Title"),
                "authors": info.get("authors", ["Unknown Author"]),
                "description": info.get("description", "No description available."),
                "thumbnail": info.get("imageLinks", {}).get("thumbnail", "https://via.placeholder.com/100x150"),
                "info_link": info.get("infoLink", "#")
            })

        return results

    except Exception as e:
        print("❌ Google Books error:", e)
        return []
