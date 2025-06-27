import requests

def get_books_by_genre(query):
    google_results = fetch_from_google_books(query)
    if google_results:
        print("✅ Google Books results used")
        return google_results
    else:
        print("⚠️ Falling back to Open Library")
        return fetch_from_open_library(query)

# 1️⃣ Google Books (No API key)
def fetch_from_google_books(query):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"
        response = requests.get(url)
        response.raise_for_status()
        books = response.json().get("items", [])
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

        return results if results else None

    except Exception as e:
        print("Google Books error:", e)
        return None

# 2️⃣ Open Library (Fallback)
def fetch_from_open_library(query):
    try:
        url = f"https://openlibrary.org/search.json?q={query}&limit=5"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("docs", [])
        results = []

        for book in data:
            title = book.get("title", "Unknown Title")
            authors = book.get("author_name", ["Unknown Author"])
            cover_id = book.get("cover_i")
            thumbnail = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else "https://via.placeholder.com/100x150"
            key = book.get("key", "")
            info_link = f"https://openlibrary.org{key}"
            results.append({
                "title": title,
                "authors": authors,
                "description": "No description available from Open Library.",
                "thumbnail": thumbnail,
                "info_link": info_link
            })

        return results if results else None

    except Exception as e:
        print("Open Library error:", e)
        return []
