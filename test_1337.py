import requests
from bs4 import BeautifulSoup

url = "https://1337pro.com/en/cs2/match-results"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

try:
    print(f"Fetching {url}...")
    resp = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.get_text()
        print(text[:1000])
        
        # Check for map names
        maps = ["Mirage", "Inferno", "Nuke", "Ancient", "Anubis"]
        found = [m for m in maps if m in text]
        print(f"Maps found: {found}")
except Exception as e:
    print(f"Error: {e}")
