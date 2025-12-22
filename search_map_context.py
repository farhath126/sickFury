import re

with open('debug_cs_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Search for "Map " followed by digit
matches = list(re.finditer(r'Map\s*\d+', content, re.IGNORECASE))
print(f"Found {len(matches)} 'Map X' instances.")

for m in matches:
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 50)
    print(f"Context: ...{content[start:end]}...")
    
# Search for just "maps"
if "maps" in content.lower():
    print("Found 'maps' in content.")
    
# Check for "veto"
if "veto" in content.lower():
    print("Found 'veto' in content.")
