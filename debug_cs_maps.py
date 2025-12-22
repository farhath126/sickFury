import requests
from bs4 import BeautifulSoup
import re

url = "https://www.gosugamers.net/counterstrike/matches/results"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

try:
    # 1. Get List
    print("Fetching results list...")
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.content, 'html.parser')
    link = soup.find('a', href=re.compile(r'/counterstrike/tournaments/.*/matches/'))
    
    if link:
        match_url = "https://www.gosugamers.net" + link['href']
        print(f"Fetching detail match: {match_url}")
        
        # 2. Get Detail
        resp_detail = requests.get(match_url, headers=headers, timeout=10)
        with open('debug_cs_detail.html', 'wb') as f:
            f.write(resp_detail.content)
        print("Saved debug_cs_detail.html")
    else:
        print("No match links found.")

except Exception as e:
    print(f"Error: {e}")
