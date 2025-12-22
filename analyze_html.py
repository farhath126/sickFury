with open("debug_cric.html", "r", encoding="utf-8") as f:
    content = f.read()

print(f"Total length: {len(content)}")

# Find "Live Score" location
idx = content.find("Live Score")
if idx != -1:
    print(f"Found 'Live Score' at {idx}")
    print(content[idx-500:idx+500])
else:
    print("Could not find 'Live Score'")

# Find "cb-col"
idx = content.find("cb-col")
if idx != -1:
    print(f"Found 'cb-col' at {idx}")
    print(content[idx-200:idx+200])

# Find class names in <a> tags
import re
links = re.findall(r'<a[^>]+class="([^"]+)"[^>]*>', content)
print(f"Found {len(links)} class attributes in <a> tags")
if links:
    print(links[:10])
