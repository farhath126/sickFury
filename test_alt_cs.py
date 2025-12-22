import requests
from bs4 import BeautifulSoup

urls = [
    "https://esportlivescore.com/l_en_g_csgo.html",
    "https://game-tournaments.com/csgo/matches"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

for url in urls:
    try:
        print(f"Testing {url}...")
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            if "Mirage" in resp.text or "Inferno" in resp.text:
                print(f"SUCCESS: Found map names in {url}")
            else:
                print(f"No specific map names found in {url} text.")
    except Exception as e:
        print(f"Error {url}: {e}")
