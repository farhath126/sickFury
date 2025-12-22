from bs4 import BeautifulSoup

def parse_match_element(el):
    text = el.get_text(" | ", strip=True)
    # text looks like: "West Indies tour of New Zealand, 2025 | 3rd Test • Mount Maunganui... | New Zealand | NZ | 575-8 d & 306-2 d | West Indies | WI | 420 & 138 | New Zealand won by 323 runs"
    parts = text.split(" | ")
    
    title = parts[0] if parts else "Unknown"
    status = parts[-1] if parts else "Unknown"
    
    # Try to find teams and scores
    # This is a bit heuristic based on the dump
    score_main = " vs ".join(parts[1:3]) if len(parts) > 2 else ""
    # "New Zealand | NZ | 575... | West Indies | WI | 420..."
    
    return {
        "title": title,
        "status": status,
        "raw": text
    }

with open("debug_cric.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# New logic: valid match cards are <a> tags with 'p-3'
cards = soup.find_all('a', class_=lambda x: x and 'p-3' in x.split())
print(f"Found {len(cards)} cards")

for i, card in enumerate(cards):
    print(f"--- Match {i+1} ---")
    data = parse_match_element(card)
    print(data['raw'])
    print("-" * 20)
