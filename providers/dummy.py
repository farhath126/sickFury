from typing import List
import random
import time
from core.state import MatchData
from providers.base import SportsProvider

class DummyCricketProvider(SportsProvider):
    def get_sport_name(self) -> str:
        return "Cricket"

    def get_matches(self) -> List[MatchData]:
        # Simulate live score changes
        runs = 120 + int((time.time() % 60) // 2)
        
        return [
            MatchData(
                id="1",
                sport="Cricket",
                title="IND vs AUS",
                status="LIVE",
                score_main=f"IND {runs}/3",
                score_sub="AUS 250",
                details="Overs: 15.2 - Kohli 45*"
            ),
            MatchData(
                id="2",
                sport="Cricket",
                title="ENG vs NZ",
                status="UPCOMING",
                score_main="00:00",
                score_sub="",
                details="Starts in 2h"
            )
        ]
