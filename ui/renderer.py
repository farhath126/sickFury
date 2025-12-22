from PIL import Image, ImageDraw, ImageFont
from core.state import AppState
import config

class Renderer:
    def __init__(self):
        self.width = config.DISPLAY_WIDTH
        self.height = config.DISPLAY_HEIGHT
        # Using default font for now, can load .ttf later
        self.font = ImageFont.load_default()
        
    def _draw_list_view(self, draw: ImageDraw, state: AppState):
        y = 0
        draw.text((2, y), f"[{state.current_sport}]", fill=255, font=self.font)
        y += 12
        draw.line((0, y, self.width, y), fill=255)
        y += 4
        
        # Draw visible window
        start_idx = state.list_scroll_offset
        max_visible = 7
        end_idx = min(len(state.matches), start_idx + max_visible)
        
        for i in range(start_idx, end_idx):
            match = state.matches[i]
            prefix = "> " if i == state.selected_match_index else "  "
            line_text = f"{prefix}{match.title} | {match.score_main}"
            draw.text((0, y), line_text, fill=255, font=self.font)
            y += 12

    def _draw_detail_view(self, draw: ImageDraw, state: AppState):
        if not state.matches:
            draw.text((10, 50), "No Matches", fill=255, font=self.font)
            return

        match = state.matches[state.selected_match_index]
        offset = state.detail_scroll_offset
        
        # Header - always fixed or scrolling? 
        # Usually easier if header stays fixed, but let's scroll everything for simplicity first,
        # OR keep "SickFury Pager" bar fixed.
        
        draw.text((2, 0), "SickFury Pager - Details", fill=255, font=self.font)
        draw.line((0, 12, self.width, 12), fill=255)
        
        # Content starts at y=20, minus offset
        base_y = 20 - offset
        y = base_y
        
        def draw_text_wrapped(text, font, draw, x, y, width_chars=40):
            import textwrap
            lines = textwrap.wrap(text, width=width_chars)
            for line in lines:
                if y > 12 and y < self.height: # Simple clipping
                    draw.text((x, y), line, fill=255, font=font)
                y += 12
            return y

        # Title
        y = draw_text_wrapped(f"Match: {match.title}", self.font, draw, 5, y)
        y += 5
        
        # Status
        y = draw_text_wrapped(f"Status: {match.status}", self.font, draw, 5, y)
        y += 5

        # Big Score
        y = draw_text_wrapped(match.score_main, self.font, draw, 5, y)
        
        # Sub Score
        y = draw_text_wrapped(match.score_sub, self.font, draw, 5, y)
        y += 5
        
        # Details (Batsmen etc) - Likely long
        y = draw_text_wrapped(match.details, self.font, draw, 5, y, width_chars=35)
        
        # Scroll Indicator (Bottom right)
        if offset > 0:
            draw.text((self.width - 10, self.height - 12), "^", fill=255, font=self.font)
        draw.text((self.width - 10, self.height - 6), "v", fill=255, font=self.font)


    def _draw_menu_view(self, draw: ImageDraw, state: AppState):
        draw.text((2, 0), "SickFury Pager", fill=255, font=self.font)
        draw.line((0, 12, self.width, 12), fill=255)
        
        y = 30
        for idx, item in enumerate(state.menu_items):
            prefix = "> " if idx == state.selected_menu_index else "  "
            draw.text((10, y), f"{prefix}{item}", fill=255, font=self.font)
            y += 15

    def render(self, state: AppState) -> Image.Image:
        # Create blank canvas (Binary color mode '1' or RGB)
        # Using RGB for easy PC viz, assume converted to 1-bit by Pi driver if needed
        image = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(image)
        
        if state.view_mode == "MENU":
            self._draw_menu_view(draw, state)
        elif state.view_mode == "LIST":
            self._draw_list_view(draw, state)
        elif state.view_mode == "DETAIL":
            self._draw_detail_view(draw, state)
            
        return image
