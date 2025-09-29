# tools.py
from langchain_community.tools import DuckDuckGoSearchRun, YouTubeSearchTool
from langchain_community.utilities import (
    DuckDuckGoSearchAPIWrapper,
    WikipediaAPIWrapper,
    ArxivAPIWrapper,
    OpenWeatherMapAPIWrapper,
)
import requests



# -----------------------
#  Multi Web Search
# -----------------------
def multi_web_search(query: str) -> str:
    """Run DuckDuckGo, Wikipedia, and Arxiv searches together."""
    try:
        wrapper = DuckDuckGoSearchAPIWrapper(backend="lite")
        ddg_search = DuckDuckGoSearchRun(api_wrapper=wrapper)
        wiki = WikipediaAPIWrapper()
        arxiv = ArxivAPIWrapper()

        results = []
        results.append("DuckDuckGo: " + ddg_search.run(query))
        results.append("Wikipedia: " + wiki.run(query))
        results.append("Arxiv: " + arxiv.run(query))

        return "\n\n".join(results)
    except Exception as e:
        return f"Search error: {e}"


# -----------------------
#  Video Search
# -----------------------
def youtube_search(query: str) -> str:
    """Search YouTube for videos."""
    try:
        yt = YouTubeSearchTool()
        return yt.run(query)
    except Exception as e:
        return f"YouTube error: {e}"


# -----------------------
#  Weather Tool
# -----------------------
def weather_search(query: str, api_key: str) -> str:
    """Get weather information using OpenWeather API."""
    try:
        weather = OpenWeatherMapAPIWrapper(openweathermap_api_key=api_key)
        return weather.run(query)
    except Exception as e:
        return f"Weather error: {e}"


# -----------------------
#  News Tool
# -----------------------
def news_search(query: str, api_key: str) -> str:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": api_key,
        "pageSize": 5,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    articles = data.get("articles", [])
    out = []
    for art in articles:
        title = art.get("title")
        url = art.get("url")
        out.append(f"{title} — {url}")
    return "\n".join(out) or "No news found."


