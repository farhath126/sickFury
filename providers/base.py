from abc import ABC, abstractmethod
from typing import List, Dict
from core.state import MatchData

class SportsProvider(ABC):
    @abstractmethod
    def get_matches(self) -> List[MatchData]:
        """Fetch current list of matches."""
        pass
    
    @abstractmethod
    def get_sport_name(self) -> str:
        """Return the name of the sport this provider handles."""
        pass
