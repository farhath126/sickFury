import requests
from bs4 import BeautifulSoup
from typing import List
from core.state import MatchData
from providers.base import SportsProvider
import time

class CricketProvider(SportsProvider):
    def __init__(self):
        self.base_url = "https://www.cricbuzz.com/cricket-match/live-scores"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }

    def get_sport_name(self) -> str:
        return "Cricket"

    def _get_batsmen_details(self, match_id: str) -> str:
        """Fetch individual match page to get batsmen details for live matches."""
        try:
            url = f"https://www.cricbuzz.com/live-cricket-scores/{match_id}"
            resp = requests.get(url, headers=self.headers, timeout=5)
            if resp.status_code != 200: return ""
            
            soup = BeautifulSoup(resp.content, 'html.parser')
            # Look for the batsmen rows in the mini-scorecard
            # Targeted class: 'flex justify-between gap-8' seems unique to these rows in the tailwind css
            rows = soup.find_all('div', class_=lambda x: x and 'justify-between' in x and 'gap-8' in x)
            
            batsmen = []
            for row in rows:
                cols = row.find_all('div')
                if len(cols) >= 2:
                    name = cols[0].get_text(strip=True)
                    score = cols[1].get_text(strip=True)
                    # Simple validation: score usually has parenthesis like 12(15)
                    if '(' in score:
                        batsmen.append(f"{name} {score}")
            
            if batsmen:
                return " | " + ", ".join(batsmen)
            return ""
        except Exception as e:
            print(f"Error fetching details for {match_id}: {e}")
            return ""

    def get_matches(self) -> List[MatchData]:
        matches = []
        import re
        import json
        
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"Cricbuzz failed: {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, 'html.parser')

            # Strategy 1: Parse Next.js embedded JSON data
            target_script = None
            for s in soup.find_all('script'):
                if s.string and 'matchScore' in s.string:
                    target_script = s.string
                    break
            
            if target_script:
                # Basic unescape: turn \" into "
                clean_script = target_script.replace('\\"', '"').replace('\\\\', '\\')
                
                # Robust Regex Loop
                # We find every matchId, then look ahead in the string to find details
                # This treats the JSON as a long string and finds patterns near the ID
                
                # Find all matchId locations
                id_matches = list(re.finditer(r'"matchId":(\d+)', clean_script))
                
                for i, match in enumerate(id_matches):
                    try:
                        mid = match.group(1)
                        if mid in [m.id for m in matches]: continue
                        
                        start_idx = match.start()
                        # Define a lookahead window. 
                        # Matches are adjacent, so we can stop at the next matchId or unreasonable length
                        # But finding the *exact* next matchId helps define the window
                        
                        end_idx = id_matches[i+1].start() if i + 1 < len(id_matches) else len(clean_script)
                        # Cap window size to 2500 chars to be safe (typical match data is < 1000)
                        if end_idx - start_idx > 3000:
                            end_idx = start_idx + 3000
                            
                        chunk = clean_script[start_idx:end_idx]
                        
                        # Status & State
                        status_match = re.search(r'"status":"(.*?)"', chunk)
                        status = status_match.group(1) if status_match else "In Progress"
                        
                        state_match = re.search(r'"state":"(.*?)"', chunk)
                        state = state_match.group(1) if state_match else ""
                        
                        # If match is Live (not Complete/Preview/Upcoming), fetch detailed batsmen info
                        bat_details = ""
                        non_live_states = ["Complete", "Preview", "Upcoming", "Abandon", "No Result"]
                        if state and state not in non_live_states:
                            bat_details = self._get_batsmen_details(mid)

                        # Teams
                        # team1 defined, then team2 usually
                        t1_match = re.search(r'"team1":\{.*?"teamSName":"(.*?)"', chunk)
                        t2_match = re.search(r'"team2":\{.*?"teamSName":"(.*?)"', chunk)
                        
                        t1s = t1_match.group(1) if t1_match else "T1"
                        t2s = t2_match.group(1) if t2_match else "T2"
                        
                        # Scores
                        # Look for "matchScore":{ ... "team1Score": ... } within the chunk
                        # Since chunk is isolated to this match, simpler regex works
                        
                        def get_score_text(team_key, source):
                            # regex for "team1Score":{ ... "runs":123 ... }
                            start = source.find(f'"{team_key}":')
                            if start == -1: return ""
                            
                            sub = source[start:start+400]
                            r_match = re.search(r'"runs":(\d+)', sub)
                            if not r_match: return ""
                            runs = r_match.group(1)
                            
                            w_match = re.search(r'"wickets":(\d+)', sub)
                            wkts = w_match.group(1) if w_match else "0"
                            
                            o_match = re.search(r'"overs":([\d\.]+)', sub)
                            overs = f" ({o_match.group(1)})" if o_match else ""

                            if wkts == "10": return f"{runs}{overs}"
                            return f"{runs}-{wkts}{overs}"

                        s1 = get_score_text("team1Score", chunk)
                        s2 = get_score_text("team2Score", chunk)
                        
                        main_score = f"{t1s} {s1}" if s1 else t1s
                        sub_score = f"{t2s} {s2}" if s2 else t2s
                        
                        final_details = f"{status}{bat_details}"
                        
                        matches.append(MatchData(
                            id=mid,
                            sport="Cricket",
                            title=f"{t1s} vs {t2s}"[:20],
                            status=status[:20] if len(status) > 20 else status,
                            score_main=main_score,
                            score_sub=sub_score,
                            details=final_details
                        ))
                    except Exception as e:
                        # print(f"Chunk parse error: {e}") 
                        continue
            
            if not matches:
                 print("JSON Regex Parsing failed, using HTML fallback")
                 return self.get_matches_html_fallback(soup)
                 
        except Exception as e:
            print(f"Scraping error: {e}")
            return []
            
        return matches

    def get_matches_html_fallback(self, soup) -> List[MatchData]:
        matches_dict = {}
        cards = soup.find_all('a', href=lambda x: x and '/live-cricket-scores/' in x)
        
        for el in cards:
            try:
                href = el.get('href', '')
                parts_url = href.split('/')
                if len(parts_url) >= 3 and parts_url[2].isdigit():
                    match_id = parts_url[2]
                else:
                    continue

                text = el.get_text(" | ", strip=True)
                parts = text.split(" | ")
                
                match_data = None
                is_rich = False

                if len(parts) >= 7:
                    # Rich/Featured Card
                    title = parts[0]
                    t1_short = parts[2]
                    t1_score = parts[3]
                    t2_short = parts[5]
                    t2_score = parts[6]
                    status = parts[7] if len(parts) > 7 else parts[-1]
                    
                    match_data = MatchData(
                        id=match_id,
                        sport="Cricket",
                        title=title[:20],
                        status=status[:20] if len(status) > 20 else status,
                        score_main=f"{t1_short} {t1_score}",
                        score_sub=f"{t2_short} {t2_score}",
                        details=status
                    )
                    is_rich = True
                
                elif len(parts) >= 2:
                    # Compact Card
                    title_attr = el.get('title', '')
                    if title_attr:
                        title = title_attr.split(',')[0]
                    else:
                        title = parts[0]
                    
                    if " - " in title_attr:     
                         status = title_attr.split(" - ")[-1]
                    elif len(parts) >= 3:
                         status = parts[-1] 
                    else:
                         status = "Preview" if "Preview" in title_attr else "In Progress"
                    
                    # Cannot scrape detailed scores easily from list view for these
                    match_data = MatchData(
                        id=match_id,
                        sport="Cricket",
                        title=title[:20],
                        status=status[:20] if len(status) > 20 else status,
                        score_main=status, 
                        score_sub="",
                        details=status
                    )

                if match_data:
                    if match_id not in matches_dict:
                        matches_dict[match_id] = (is_rich, match_data)
                    else:
                        existing_is_rich, _ = matches_dict[match_id]
                        if is_rich and not existing_is_rich:
                            matches_dict[match_id] = (is_rich, match_data)
            
            except Exception:
                continue
                
        return [data for _, data in matches_dict.values()]
