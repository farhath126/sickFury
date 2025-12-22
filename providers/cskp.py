import requests
from bs4 import BeautifulSoup
import re
from typing import List
from core.state import MatchData

class CSKPProvider:
    """
    Provider for Counter-Strike 2 scores.
    Scrapes GosuGamers for match listings.
    """
    
    URL_UPCOMING = "https://www.gosugamers.net/counterstrike/matches"
    URL_RESULTS = "https://www.gosugamers.net/counterstrike/matches/results"
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    def get_sport_name(self) -> str:
        return "CS2"

    def get_matches(self) -> List[MatchData]:
        all_matches = []
        
        # We fetch both sources
        sources = [
            (self.URL_UPCOMING, "Upcoming"),
            (self.URL_RESULTS, "Past")
        ]
        
        for url, source_type in sources:
            try:
                resp = requests.get(url, headers=self.HEADERS, timeout=6)
                if resp.status_code != 200: continue
                
                soup = BeautifulSoup(resp.content, 'html.parser')
                links = soup.find_all('a', href=re.compile(r'/counterstrike/tournaments/.*/matches/'))
                
                for i, link in enumerate(links):
                    try:
                        text_content = link.get_text(" ", strip=True)
                        
                        # Teams
                        teams = []
                        for elem in link.find_all(attrs={"aria-label": True}):
                            label = elem['aria-label']
                            teams.append(label)
                        
                        # Dedupe strictly preserving order
                        seen = set()
                        teams_clean = [x for x in teams if not (x in seen or seen.add(x))]
                        
                        if len(teams_clean) >= 2:
                            t1 = teams_clean[0]
                            t2 = teams_clean[1]
                        else:
                            # Fallback from text is risky but try
                            if " VS " in text_content:
                                parts = text_content.split(" VS ")
                                t1 = parts[0].split()[-1]
                                t2 = parts[1].split()[0]
                            elif " : " in text_content: # For results
                                # Text: Tournament Data TeamA 3 : 0 TeamB
                                # Hard to parse teams purely from text without delimiters
                                t1, t2 = "Team A", "Team B"
                            else:
                                t1, t2 = "TBD", "TBD"

                        # Clean Text Content
                        # "Tournament Name TeamA Score : Score TeamB"
                        # Example: "Cajunto Copa do Brasil - Main Event - Playoffs 9z 3 : 0 ShindeN"
                        
                        # Status & Score
                        score_main = "vs"
                        status = "Upcoming"
                        
                        # Check for Result Score (e.g., "3 : 0")
                        score_match = re.search(r'(\d+)\s*:\s*(\d+)', text_content)
                        
                        # Extract Tournament Name (Everything before the first team or score)
                        # This is tricky without knowing team names exactly in text
                        # But we have T1, T2 from aria-labels
                        
                        details = text_content
                        
                        if score_match:
                            s1 = score_match.group(1)
                            s2 = score_match.group(2)
                            score_main = f"{s1} - {s2}"
                            status = "FT" if source_type == "Past" else "LIVE"
                            if source_type == "Upcoming": status = "LIVE"
                            
                            # Try to clean details
                            # Remove the score and team names from details roughly
                            # Regex replace team names and score with empty
                            clean_det = text_content
                            clean_det = clean_det.replace(t1, "").replace(t2, "")
                            clean_det = re.sub(r'\d+\s*:\s*\d+', '', clean_det)
                            clean_det = clean_det.strip()
                            # Often leaves " - - " or similar
                            clean_det = re.sub(r'^\s*-\s*', '', clean_det)
                            clean_det = re.sub(r'\s*-\s*$', '', clean_det)
                            details = clean_det[:60]
                        
                        elif "Live" in text_content or "LIVE" in text_content:
                            status = "LIVE"
                            score_main = "0 - 0"
                        
                        else:
                            # Upcoming time
                            time_match = re.search(r'(\d+)\s*h\s*(\d+)\s*m', text_content)
                            if time_match:
                                status = f"in {time_match.group(1)}h{time_match.group(2)}m"
                            elif "Upcoming" in text_content:
                                status = "Upcoming"
                            elif source_type == "Past":
                                status = "FT"

                        # Formatting
                        title = f"{t1} vs {t2}"
                        mid = f"cs_{abs(hash(title + status))}" 
                        
                        # Map Names Detection
                        # We check for known map names in the text content
                        known_maps = ["Mirage", "Inferno", "Nuke", "Vertigo", "Ancient", "Anubis", "Overpass", "Dust2", "Train"]
                        found_maps = []
                        for m in known_maps:
                            # Simple check, might need regex for boundary if matches within words (unlikely for these names)
                            if m in text_content:
                                found_maps.append(m)
                        
                        if found_maps:
                            # Prepend maps to details
                            map_str = "Maps: " + ", ".join(found_maps)
                            details = f"{map_str} | {details}"
                            
                        # parse "Best of X" if present
                        if "Best of" in text_content:
                            details += " (BO" + text_content.split("Best of")[1].strip()[0] + ")" # Roughly

                        all_matches.append(MatchData(
                            id=mid,
                            sport="CS2",
                            title=title,
                            status=status,
                            score_main=score_main,
                            score_sub="", # Could put BO3 here
                            details=details
                        ))
                        
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"CS Scrape Error ({source_type}): {e}")

        # Sort: LIVE -> Upcoming -> FT
        def sort_key(m):
            if m.status == "LIVE": return 0
            if "in " in m.status: return 1
            if m.status == "Upcoming": return 2
            return 3 # FT
            
        all_matches.sort(key=sort_key)
        
        return all_matches
