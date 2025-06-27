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
            return []

        results = []
        for book in books:
            work_key = book.get("key", "")
            title = book.get("title", "Unknown Title")
            authors = book.get("author_name", ["Unknown Author"])
            cover_id = book.get("cover_i")
            thumbnail = (
                f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                if cover_id else "https://via.placeholder.com/100x150"
            )
            info_link = f"https://openlibrary.org{work_key}"

            # 📝 Fetch description
            description = "No description available."
            if work_key:
                try:
                    work_data = requests.get(f"https://openlibrary.org{work_key}.json", timeout=10).json()
                    desc = work_data.get("description", "")
                    if isinstance(desc, dict):
                        description = desc.get("value", description)
                    elif isinstance(desc, str):
                        description = desc
                except:
                    pass

            results.append({
                "title": title,
                "authors": authors,
                "description": description,
                "thumbnail": thumbnail,
                "info_link": info_link
            })

        return results

    except Exception as e:
        print("Error fetching books:", e)
        return []
