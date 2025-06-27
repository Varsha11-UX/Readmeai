import requests

def get_books_by_genre(query):
    return fetch_from_open_library(query)

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
            key = book.get("key", "")
            info_link = f"https://openlibrary.org{key}"
            thumbnail = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else "https://via.placeholder.com/100x150"

            # 🔍 Fetch description from /works/<key>.json
            desc = "No description available from Open Library."
            if key:
                work_url = f"https://openlibrary.org{key}.json"
                work_response = requests.get(work_url)
                if work_response.status_code == 200:
                    work_data = work_response.json()
                    if "description" in work_data:
                        if isinstance(work_data["description"], dict):
                            desc = work_data["description"].get("value", desc)
                        else:
                            desc = work_data["description"]

            results.append({
                "title": title,
                "authors": authors,
                "description": desc,
                "thumbnail": thumbnail,
                "info_link": info_link
            })

        return results

    except Exception as e:
        print("❌ Open Library error:", e)
        return []
