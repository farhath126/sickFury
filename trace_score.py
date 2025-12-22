from bs4 import BeautifulSoup

with open("debug_cric.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find string "575-8"
target = soup.find(string=lambda t: t and "575-8" in t)
if target:
    print(f"Found '{target}'. Parents:")
    curr = target
    for i in range(10): 
        curr = curr.parent
        if curr:
            print(f"Level {i}: {curr.name} | Classes: {curr.get('class', [])} | ID: {curr.get('id', '')}")
        else:
            break
else:
    print("Not found specific score")
