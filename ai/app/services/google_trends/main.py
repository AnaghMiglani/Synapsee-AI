from serpapi import GoogleSearch
from app.core.config import SERPAPI_API_KEY


def get_google_trends_serpapi(
    keyword,
    time_range="today 12-m",
    geo="IN",
    search_type="web"
):
    gprop_map = {
        "web": "",
        "shopping": "froogle",
        "youtube": "youtube",
        "news": "news",
        "images": "images"
    }

    params = {
        "engine": "google_trends",
        "q": keyword,
        "date": time_range,
        "geo": geo,
        "gprop": gprop_map.get(search_type, ""),
        "data_type": "TIMESERIES",
        "tz": 330,
        "api_key": SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("interest_over_time", {})


POPULAR_MARKETS = {
    "anywhere": "",
    "worldwide": "",
    "global": "",

    "india": "IN",
    "delhi": "IN-DL",
    "mumbai": "IN-MH",
    "maharashtra": "IN-MH",
    "bangalore": "IN-KA",
    "karnataka": "IN-KA",
    "chennai": "IN-TN",
    "tamil nadu": "IN-TN",
    "hyderabad": "IN-TG",
    "telangana": "IN-TG",
    "kolkata": "IN-WB",
    "west bengal": "IN-WB",
    "pune": "IN-MH",
    "gujarat": "IN-GJ",
    "ahmedabad": "IN-GJ",
    "rajasthan": "IN-RJ",
    "uttar pradesh": "IN-UP",
    "noida": "IN-UP",
    "gurgaon": "IN-HR",
    "haryana": "IN-HR",
    "kerala": "IN-KL",

    "united states": "US",
    "usa": "US",
    "california": "US-CA",
    "new york": "US-NY",
    "texas": "US-TX",

    "united kingdom": "GB",
    "uk": "GB",
    "england": "GB-ENG",
    "london": "GB-ENG",

    "canada": "CA",
    "toronto": "CA-ON",

    "australia": "AU",
    "sydney": "AU-NSW",

    "germany": "DE",
    "france": "FR",
    "italy": "IT",
    "spain": "ES",

    "japan": "JP",
    "south korea": "KR",
    "china": "CN",

    "brazil": "BR",
    "mexico": "MX",

    "singapore": "SG",
    "uae": "AE",
    "dubai": "AE-DU",

    "indonesia": "ID",
    "vietnam": "VN"
}
