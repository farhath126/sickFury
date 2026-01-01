import time
import threading
from core.state import AppState
from core.events import *
from hal.pc_impl import PCDisplay, PCInput
from providers.cricket import CricketProvider
from providers.football import FootballProvider
from providers.cskp import CSKPProvider
from ui.renderer import Renderer
import config

class App:
    def __init__(self):
        self.state = AppState()
        
        # Initialize HAL (Hardcoded to PC for Phase 1)
        self.display = PCDisplay(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        self.input = PCInput()
        
        # Initialize Providers
        self.providers = {
            "Cricket": CricketProvider(),
            "Football": FootballProvider(),
            "CS2": CSKPProvider()
        }
        self.current_provider = self.providers["Cricket"] # Default but overridden by menu
        
        # Initialize UI
        self.renderer = Renderer()

    def _fetch_data(self):
        """Worker method to fetch data in background."""
        while self.state.running:
            try:
                # Only fetch if we are NOT in menu (or fetch background?)
                # We can fetch background for current sport
                if self.state.view_mode != "MENU":
                    new_matches = self.current_provider.get_matches()
                    # print(f"Fetched {len(new_matches)} matches.")
                    self.state.matches = new_matches
                    self.state.last_update_time = time.time()
            except Exception as e:
                print(f"Error fetching data: {e}")
            
            time.sleep(config.REFRESH_INTERVAL)

    def _handle_input(self):
        events = self.input.get_events()
        for event in events:
            if event == EVT_QUIT:
                self.state.running = False
            
            elif event == EVT_BTN_DOWN:
                if self.state.view_mode == "MENU":
                    self.state.selected_menu_index = (self.state.selected_menu_index + 1) % len(self.state.menu_items)
                
                elif self.state.view_mode == "LIST" and self.state.matches:
                    self.state.selected_match_index = (self.state.selected_match_index + 1) % len(self.state.matches)
                    
                    # Scroll Logic (naive assumption of 7 items)
                    items_visible = 7
                    if self.state.selected_match_index >= self.state.list_scroll_offset + items_visible:
                        self.state.list_scroll_offset = self.state.selected_match_index - items_visible + 1
                    # Wrap around handling
                    if self.state.selected_match_index == 0:
                        self.state.list_scroll_offset = 0
                        
                elif self.state.view_mode == "DETAIL":
                    self.state.detail_scroll_offset += 10

            # 2-Button Logic (BTN_A = Next/Scroll, BTN_B = Select/Action)
            if event == EVT_BTN_A:
                # NEXT / SCROLL
                if self.state.view_mode == "MENU":
                    self.state.selected_menu_index = (self.state.selected_menu_index + 1) % len(self.state.menu_items)
                
                elif self.state.view_mode == "LIST":
                    # List size = matches + 1 (for Back button)
                    list_size = len(self.state.matches) + 1
                    self.state.selected_match_index = (self.state.selected_match_index + 1) % list_size
                    
                    # Scroll Logic (Keep cursor visible)
                    items_visible = 7
                    # If cursor goes below visible window, move offset
                    if self.state.selected_match_index >= self.state.list_scroll_offset + items_visible:
                        self.state.list_scroll_offset += 1
                    # If cursor wraps to top (0), reset offset
                    if self.state.selected_match_index == 0:
                        self.state.list_scroll_offset = 0

                elif self.state.view_mode == "DETAIL":
                    # Scroll Down
                    # Need max height? Hard to know without renderer feedback, but we can guess or just let it grow.
                    # We can wrap to top if user scrolls too far?
                    # Let's just scroll down indefinitely for now, or maybe wrap at some point?
                    # A "Loop to Top" behavior is good for single-button scrolling.
                    self.state.detail_scroll_offset += 10
                    # For now no max check, user can scroll endlessly or we need a way to know content height.
            
            elif event == EVT_BTN_B:
                # SELECT / ACTION
                if self.state.view_mode == "MENU":
                    # Select Sport
                    sport = self.state.menu_items[self.state.selected_menu_index]
                    self.state.current_sport = sport
                    self.current_provider = self.providers[sport]
                    self.state.matches = [] 
                    self.state.view_mode = "LIST"
                    self.state.selected_match_index = 1 # Start at first match, 0 is Back
                    self.state.list_scroll_offset = 0
                    threading.Thread(target=self._force_fetch).start()

                elif self.state.view_mode == "LIST":
                    if self.state.selected_match_index == 0:
                        # BACK Selected
                        self.state.view_mode = "MENU"
                        self.state.selected_match_index = 0
                    else:
                        # Match Selected (Index - 1)
                        if self.state.matches:
                            self.state.view_mode = "DETAIL"
                            self.state.detail_scroll_offset = 0

                elif self.state.view_mode == "DETAIL":
                    # Back to List
                    self.state.view_mode = "LIST"
            
            # Legacy/Dev Controls
            # Legacy/Dev Controls
            elif event == EVT_BTN_BACK:
                 if self.state.view_mode == "DETAIL":
                     self.state.view_mode = "LIST"
                 elif self.state.view_mode == "LIST":
                     self.state.view_mode = "MENU"
                     self.state.matches = []

    def _force_fetch(self):
        try:
             new = self.current_provider.get_matches()
             self.state.matches = new
        except: pass

    def run(self):
        print("Starting SickFury Pager...")
        self.display.init()
        self.input.init()
        
        # Start Data Thread
        data_thread = threading.Thread(target=self._fetch_data, daemon=True)
        data_thread.start()
        
        # Main Loop
        clock_period = 1.0 / config.FRAMERATE
        
        while self.state.running:
            start_time = time.time()
            
            # 1. Handle Input
            self._handle_input()
            
            # 2. Update State (Data thread does this async, main thread logic here if needed)
            
            # 3. Render
            image = self.renderer.render(self.state)
            self.display.draw_image(image)
            
            # 4. Sleep
            elapsed = time.time() - start_time
            if elapsed < clock_period:
                time.sleep(clock_period - elapsed)

        print("Shutting down.")
