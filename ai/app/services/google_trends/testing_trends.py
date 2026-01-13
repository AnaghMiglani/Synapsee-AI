from ai.app.services.google_trends.main import get_google_trends_serpapi, POPULAR_MARKETS
results = get_google_trends_serpapi(
    keyword="sweater",
    time_range="today 12-m",
    geo="IN",
    search_type="shopping"
)
print(results)