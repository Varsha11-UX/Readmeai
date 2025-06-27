import requests

def get_books_by_genre(query):
    try:
        if not query or len(query.strip()) < 3:
            query = "fiction"

        url = f"https://openlibrary.org/search.json?q={query}&limit=5"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        books = response.json().get("docs", [])
        if not books:
            print("DEBUG: No books found on Open Library.")
            return []

        results = []
        for book in books:
            results.append({
                "title": book.get("title", "Unknown Title"),
                "authors": book.get("author_name", ["Unknown Author"]),
                "description": "No description available from Open Library.",
                "thumbnail": (
                    f"https://covers.openlibrary.org/b/id/{book.get('cover_i')}-M.jpg"
                    if book.get("cover_i") else "https://via.placeholder.com/100x150"
                ),
                "info_link": f"https://openlibrary.org{book.get('key', '')}"
            })

        return results

    except Exception as e:
        print("Error fetching books:", e)
        return []
