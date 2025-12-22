import requests
from bs4 import BeautifulSoup

url = "https://www.cricbuzz.com/cricket-match/live-scores"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.content, "html.parser")
with open("debug_cric.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())
print("Saved debug_cric.html")
