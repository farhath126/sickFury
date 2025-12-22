from bs4 import BeautifulSoup

with open('debug_cs_detail.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text('\n', strip=True)

print(text[:2000])

# Look for score breakdown
# Usually something like "13 - 11"
import re
scores = re.findall(r'\d+\s-\s\d+', text)
print(f"Scores found: {scores}")

# Look for specific keywords associated with maps
keywords = ["Map", "Pick", "Ban", "Mirage", "Inferno", "Nuke", "Vertigo", "Ancient", "Anubis", "Overpass", "Dust2"]
for k in keywords:
    if k.lower() in text.lower():
        print(f"Found keyword: {k}")
