import requests
from bs4 import BeautifulSoup
import re

url = "https://www.gosugamers.net/counterstrike/matches/results"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

try:
    print(f"Fetching {url}...")
    resp = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        links = soup.find_all('a', href=re.compile(r'/counterstrike/tournaments/.*/matches/'))
        print(f"Found {len(links)} match links.")
        
        for i, link in enumerate(links[:5]):
            print(f"--- Match {i} ---")
            text_content = link.get_text(" ", strip=True)
            print(f"Text: {text_content}")
            
            # Try to find scores
            # In results, scores are usually visible
            # e.g. "TeamA 2 - 1 TeamB" or raw numbers
            
            teams = []
            for elem in link.find_all(attrs={"aria-label": True}):
                label = elem['aria-label']
                teams.append(label)
            teams = list(dict.fromkeys(teams))
            print(f"Teams from aria-label: {teams}")
            
            # Check for score numbers
            # In HTML they might be in specific spans
            # Let's see if we can perform a quick regex on text for "X - Y" or similar
            
except Exception as e:
    print(f"Error: {e}")
