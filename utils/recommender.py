import requests

def get_books_by_genre(query):
    try:
        # Fallback if query is empty or vague
        if not query or len(query.strip()) < 3:
            query = "fiction"

        # Replace spaces with + for better API query
        search_term = query.replace(" ", "+")

        url = f"https://www.googleapis.com/books/v1/volumes?q={search_term}&maxResults=5"
        response = requests.get(url)
        response.raise_for_status()

        books = response.json().get("items", [])
        if not books:
            print("DEBUG: No books found for query:", query)

        results = []
        for book in books:
            volume_info = book.get("volumeInfo", {})
            results.append({
                "title": volume_info.get("title", "Unknown Title"),
                "authors": volume_info.get("authors", ["Unknown Author"]),
                "description": volume_info.get("description", "No description available."),
                "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", "https://via.placeholder.com/100x150"),
                "info_link": volume_info.get("infoLink", "#")
            })
        return results

    except Exception as e:
        print("Error fetching books:", e)
        return []
