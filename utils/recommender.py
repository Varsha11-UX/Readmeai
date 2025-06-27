import requests

def get_books_by_genre(query):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"
        response = requests.get(url)
        books = response.json().get("items", [])
        results = []

        for book in books:
            volume_info = book.get("volumeInfo", {})
            results.append({
                "title": volume_info.get("title", "Unknown Title"),
                "authors": volume_info.get("authors", ["Unknown Author"]),
                "description": volume_info.get("description", "No description available."),
                "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
                "info_link": volume_info.get("infoLink", "#")
            })
        return results
    except Exception as e:
        print("Error fetching books:", e)
        return []
