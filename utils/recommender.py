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
            work_key = book.get("key", "")
            title = book.get("title", "Unknown Title")
            authors = book.get("author_name", ["Unknown Author"])
            cover_id = book.get("cover_i")
            thumbnail = (
                f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                if cover_id else "https://via.placeholder.com/100x150"
            )
            info_link = f"https://openlibrary.org{work_key}"

            # 📝 Fetch description via /works/OLxxxW.json
            description = "No description available."
            if work_key:
                work_url = f"https://openlibrary.org{work_key}.json"
                try:
                    work_response = requests.get(work_url, timeout=10)
                    work_response.raise_for_status()
                    work_data = work_response.json()
                    desc_data = work_data.get("description", "")
                    if isinstance(desc_data, dict):
                        description = desc_data.get("value", description)
                    elif isinstance(desc_data, str):
                        description = desc_data
                except Exception as e:
                    print(f"Failed to fetch description for {title}: {e}")

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
