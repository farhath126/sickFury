from bs4 import BeautifulSoup

with open('debug_cs_gosu.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

matches = []

# Find all links to matches
# Regex for href starting with /counterstrike/tournaments/ and containing /matches/
# Or just /matches/ id
import re
match_links = soup.find_all('a', href=re.compile(r'/counterstrike/tournaments/.*/matches/'))

print(f"Found {len(match_links)} match cards.")

for link in match_links:
    try:
        # Teams are often in aria-labels or text
        # Look for elements with aria-label text
        teams = []
        for elem in link.find_all(attrs={"aria-label": True}):
            label = elem['aria-label']
            if label not in ["breadcrumb", "user-menu"]: # Filter noise
                teams.append(label)
        
        # Dedupe
        teams = list(dict.fromkeys(teams))
        
        if len(teams) >= 2:
            t1 = teams[0]
            t2 = teams[1]
        else:
            t1 = "TBD"
            t2 = "TBD"
            
        # Status/Time
        # Usually text inside a specific container or just the text of the card
        # Let's extract all text and analyze
        text = link.get_text(" ", strip=True)
        
        # Tournament usually appears
        # Time usually appears (e.g., "2h 59m")
        
        matches.append({
            "title": f"{t1} vs {t2}",
            "raw_text": text
        })
        
    except Exception as e:
        print(f"Error parsing card: {e}")

for m in matches[:5]:
    print(m)
