import requests
import json

# LaLiga (for Barca/Betis examples)
url = "http://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard"

try:
    resp = requests.get(url, timeout=10)
    data = resp.json()
    
    debug_info = []
    
    for event in data.get('events', []):
        name = event.get('name')
        match_id = event.get('id')
        
        # Only interested in matches with goals to debug
        scores = event.get('competitions', [{}])[0].get('competitors', [])
        total_score = sum(int(c.get('score', 0)) for c in scores)
        
        if total_score > 0:
            details = event.get('competitions', [{}])[0].get('details', [])
            
            # Extract ALL detail types to see what we might be missing
            events_log = []
            for d in details:
                type_text = d.get('type', {}).get('text')
                clock = d.get('clock', {}).get('displayValue')
                
                players = d.get('athletesInvolved', [])
                player_name = players[0].get('displayName') if players else "N/A"
                
                events_log.append(f"{type_text} - {player_name} ({clock})")
            
            debug_info.append({
                "match": name,
                "score": f"{scores[0]['score']}-{scores[1]['score']}",
                "raw_details": events_log
            })

    with open('debug_goals.json', 'w') as f:
        json.dump(debug_info, f, indent=2)
        
    print("Saved debug_goals.json")

except Exception as e:
    print(f"Error: {e}")
