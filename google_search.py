import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

PRIMARY_SITES = ["isro.gov.in", "celestrak.com", "unoosa.org", "n2yo.com", "esa.int", "space-track.org", "nasaspaceflight.com"]
SECONDARY_SITES = ["wikipedia.org", "space.com", "spacenews.com", "timesofindia.indiatimes.com", "thehindu.com", "business-standard.com"]

def build_query(query, site=None):
    if site:
        return f'site:{site} {query}'
    return query

def serpapi_search(query, site_filter=None):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": build_query(query, site_filter),
        "api_key": SERPAPI_KEY,
        "num": 1
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json().get("organic_results", [])
        if results:
            top_result = results[0]
            snippet = top_result.get("snippet")
            link = top_result.get("link")
            if snippet and link:
                return snippet, link
            elif link:  # fallback if only link is present
                return "No snippet available", link
            else:
                print("Result missing both snippet and link:", top_result)
    else:
        print(f"SerpAPI Error: {response.status_code}, {response.text}")

    return None, None

def search_with_trust(query, try_open_search = False):
    if not try_open_search:
        # 1. Primary sites
        for site in PRIMARY_SITES:
            result, link = serpapi_search(query, site)
            if result:
                return result, link, "primary"

        # 2. Secondary sites
        for site in SECONDARY_SITES:
            result, link = serpapi_search(query, site)
            if result:
                return result, link, "secondary"

    # 3. Open internet (fallback)
    result, link = serpapi_search(query)
    if result:
        return result, link, "tertiary"

    return None, None, "not_found"