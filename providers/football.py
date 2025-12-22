import requests
from typing import List
from core.state import MatchData
import datetime

class FootballProvider:
    """
    Provider for Football scores using ESPN public API.
    Fetches Live scores for major EU leagues and International.
    """
    
    LEAGUES = [
        ("EPL", "http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"),
        ("LaLiga", "http://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard"),
        ("Bundesliga", "http://site.api.espn.com/apis/site/v2/sports/soccer/ger.1/scoreboard"),
        ("Serie A", "http://site.api.espn.com/apis/site/v2/sports/soccer/ita.1/scoreboard"),
        ("UCL", "http://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard"),
        ("Ligue 1", "http://site.api.espn.com/apis/site/v2/sports/soccer/fra.1/scoreboard"),
    ]

    def get_sport_name(self) -> str:
        return "Football"

    def get_matches(self) -> List[MatchData]:
        matches = []
        for league_name, url in self.LEAGUES:
            try:
                # Short timeout to avoid hanging
                resp = requests.get(url, timeout=4)
                if resp.status_code != 200: continue
                
                data = resp.json()
                events = data.get('events', [])
                
                for event in events:
                    try:
                        match_id = event.get('id')
                        name = event.get('shortName') or event.get('name')
                        name = name.replace(" at ", " vs ").replace("@", "vs")
                        
                        status_obj = event.get('status', {})
                        state = status_obj.get('type', {}).get('state') # pre, in, post
                        status_detail = status_obj.get('type', {}).get('shortDetail') # 45', FT, 12:30 PM
                        
                        comp = event.get('competitions', [{}])[0]
                        competitors = comp.get('competitors', [])
                        
                        home = next((c for c in competitors if c['homeAway'] == 'home'), {})
                        away = next((c for c in competitors if c['homeAway'] == 'away'), {})
                        
                        h_team = home.get('team', {}).get('abbreviation', 'H')
                        a_team = away.get('team', {}).get('abbreviation', 'A')
                        h_score = home.get('score', '0')
                        a_score = away.get('score', '0')
                        
                        score_main = f"{h_team} {h_score} vs {a_score} {a_team}"
                        
                        # Goals Details
                        details_list = []
                        if state in ['in', 'post']:
                            # Parse events for goals
                            game_details = comp.get('details', [])
                            for d in game_details:
                                # Robust check for any scoring play (Goals, Penalties, Own Goals)
                                if d.get('scoringPlay', False):
                                    type_text = d.get('type', {}).get('text', '')
                                    
                                    # Finding player name
                                    scorer = "Unknown"
                                    players = d.get('athletesInvolved', [])
                                    if players:
                                        scorer = players[0].get('shortName', players[0].get('displayName'))
                                    
                                    # Add context (OG, P)
                                    if "Own Goal" in type_text:
                                        scorer += " (OG)"
                                    elif "Penalty" in type_text:
                                        scorer += " (P)"
                                    
                                    clock_display = d.get('clock', {}).get('displayValue', '')
                                    
                                    # Determine side (optional, but name is enough usually)
                                    details_list.append(f"{scorer} {clock_display}")
                        
                        # Format details string
                        details_str = f"[{league_name}] {status_detail}"
                        if details_list:
                            details_str += " | Goals: " + ", ".join(details_list) # Show ALL goals now
                        
                        # Status for sorting/display
                        # For 'in' (Live), we want to show the timer or 'HT'
                        display_status = status_detail
                        
                        matches.append(MatchData(
                            id=match_id,
                            sport="Football",
                            title=name,
                            status=display_status,
                            score_main=score_main,
                            score_sub=f"{league_name}",
                            details=details_str
                        ))
                    except Exception as e:
                        # print(f"Error parsing event: {e}")
                        continue
                        
            except Exception as e:
                print(f"Failed to fetch {league_name}: {e}")
                continue

        # Sort: Live ('in') first, then upcoming/recent
        def sort_key(m):
            if "'" in m.status or m.status == "HT": return 0
            if m.status == "FT": return 2
            return 1 
            
        matches.sort(key=sort_key)
        
        return matches
