import requests

def scrape_via_render(keyword: str) -> dict:
    url = "https://synapsee-ai.onrender.com/scrape"

    payload = {
        "product": keyword
    }

    response = requests.post(
        url,
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    return response.json()
