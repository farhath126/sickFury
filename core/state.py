from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class MatchData:
    id: str
    sport: str
    title: str
    status: str  # 'LIVE', 'FINISHED', 'UPCOMING'
    score_main: str
    score_sub: str
    details: str

@dataclass
class AppState:
    running: bool = True
    current_sport: str = "Cricket"
    matches: List[MatchData] = field(default_factory=list)
    selected_match_index: int = 0
    # For split screen (later)
    secondary_match_index: Optional[int] = None
    
    # UI State
    view_mode: str = "MENU" # MENU, LIST, DETAIL, SPLIT
    last_update_time: float = 0
    
    # Menu
    menu_items: List[str] = field(default_factory=lambda: ["Cricket", "Football", "CS2"])
    selected_menu_index: int = 0
    
    # Scrolling
    list_scroll_offset: int = 0
    detail_scroll_offset: int = 0
