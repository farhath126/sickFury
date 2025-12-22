import requests
from bs4 import BeautifulSoup

url = "https://liquipedia.net/counterstrike/Liquipedia:Matches"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

try:
    print(f"Fetching {url}...")
    resp = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Look for tables with matches
        # Liquipedia uses <div class="table-responsive"> or similar
        # and "wikitable"
        
        # Search for text "Mirage"
        text = soup.get_text()
        if "Mirage" in text or "Ancient" in text:
            print("Found map keywords in text!")
            
        # Print a chunk
        print(text[:1000])
        
except Exception as e:
    print(f"Error: {e}")
