from bs4 import BeautifulSoup

with open("debug_cric.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find string "New Zealand"
target = soup.find(string=lambda t: t and "New Zealand" in t)
if target:
    print("Found 'New Zealand'. Parents:")
    curr = target
    for i in range(5): # Go up 5 levels
        curr = curr.parent
        if curr:
            print(f"Level {i}: {curr.name} | Classes: {curr.get('class', [])}")
        else:
            break
else:
    print("Not found")
