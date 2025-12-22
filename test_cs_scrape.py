import requests
from bs4 import BeautifulSoup

targets = [
    ("HLTV", "https://www.hltv.org/matches"),
    ("Gosu", "https://www.gosugamers.net/counterstrike/matches"),
    ("GGScore", "https://ggscore.com/en/csgo/matches")
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

for name, url in targets:
    try:
        print(f"Testing {name}...")
        resp = requests.get(url, headers=headers, timeout=5)
        print(f"{name} Status: {resp.status_code}")
        if resp.status_code == 200:
            with open(f'debug_cs_{name.lower()}.html', 'wb') as f:
                f.write(resp.content)
            print(f"Saved debug_cs_{name.lower()}.html")
    except Exception as e:
        print(f"{name} Failed: {e}")
