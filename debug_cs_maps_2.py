import requests
from bs4 import BeautifulSoup
import re

url = "https://www.gosugamers.net/counterstrike/matches/results"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

try:
    print("Fetching results list...")
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    # Find match matches "SAW" just to be diverse
    # Loop through links
    links = soup.find_all('a', href=re.compile(r'/counterstrike/tournaments/.*/matches/'))
    
    target_link = None
    for link in links:
        if "SAW" in link.get_text() or "NiP" in link.get_text():
            target_link = link['href']
            break
            
    if not target_link and len(links) > 0:
        target_link = links[1]['href'] # Pick 2nd one
        
    if target_link:
        full_url = "https://www.gosugamers.net" + target_link
        print(f"Fetching detail match: {full_url}")
        
        resp_detail = requests.get(full_url, headers=headers, timeout=10)
        content = resp_detail.text
        
        # Check for maps
        maps = ["Mirage", "Inferno", "Nuke", "Vertigo", "Ancient", "Anubis", "Overpass", "Dust2"]
        found = []
        for m in maps:
            if m in content or m.lower() in content.lower():
                found.append(m)
        
        print(f"Maps found in {full_url}: {found}")
        
        # Save for manual inspection if needed
        with open('debug_cs_detail_2.html', 'w', encoding='utf-8') as f:
            f.write(content)
            
    else:
        print("No matches found.")

except Exception as e:
    print(f"Error: {e}")
