import requests
import json

# EPL
url = "http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"

try:
    resp = requests.get(url, timeout=10)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print("Scraped ESPN JSON successfully.")
        # Save for inspection
        with open('debug_espn_football.json', 'w') as f:
            json.dump(data, f, indent=2)
            
        # Check structure
        events = data.get('events', [])
        print(f"Found {len(events)} events.")
        if events:
            print(f"Sample: {events[0].get('name')}")
            
except Exception as e:
    print(f"Error: {e}")
