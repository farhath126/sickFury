maps = ["Mirage", "Inferno", "Nuke", "Vertigo", "Ancient", "Anubis", "Overpass", "Dust2"]

with open('debug_cs_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

found = []
for m in maps:
    if m in content:
        found.append(m)

print(f"Maps found: {found}")

# Also try to find context
import re
for m in maps:
    matches = list(re.finditer(m, content))
    for match in matches:
        start = max(0, match.start() - 50)
        end = min(len(content), match.end() + 50)
        print(f"Context for {m}: ...{content[start:end]}...")
