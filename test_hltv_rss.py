import requests
import xml.etree.ElementTree as ET

url = "https://www.hltv.org/rss/matches"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

try:
    print(f"Fetching {url}...")
    resp = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        print("Parsing RSS...")
        root = ET.fromstring(resp.content)
        count = 0
        for item in root.findall('./channel/item'):
            title = item.find('title').text
            desc = item.find('description').text
            link = item.find('link').text
            pubDate = item.find('pubDate').text
            
            print(f"Match: {title}")
            print(f"Desc: {desc}")
            print(f"Link: {link}")
            print("-" * 20)
            count += 1
            if count > 5: break
            
except Exception as e:
    print(f"Error: {e}")
