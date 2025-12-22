# SickFury Architecture Design

## High-Level Diagram

```
+---------------------------------------------------------------+
|                        Main Loop (Core)                       |
|  - Orchestraion                                               |
|  - Event Handling (State changes, input events)               |
+------------------------------+--------------------------------+
                               |
       +-----------------------+-----------------------+
       |                       |                       |
+------v------+        +-------v------+        +-------v-------+
|    Input    |        |  Data Layer  |        |      UI       |
|  Manager    |        |  (Providers) |        |    Engine     |
+------+------+        +-------+------+        +-------+-------+
       ^                       ^                       |
       |                       |                       |
+------+------+        +-------+------+        +-------v-------+
|     HAL     |        | Sports APIs  |        |     HAL       |
| (Key/GPIO)  |        | (Scrapers)   |        | (Scrn/OLED)   |
+-------------+        +--------------+        +---------------+
```

## Module Breakdown

### 1. Core (`core/`)
Responsible for gluing everything together.
- **`App`**: The main class that initializes HAL, Providers, and UI. Runs the main event loop.
- **`StateManager`**: Holds the "truth". Current selected sport, active matches, split-screen mode status, latest score caches.
- **`EventBus`**: Simple publish/subscribe system. (e.g., `Input -> EventBus -> App -> UI`).

### 2. Hardware Abstraction Layer (`hal/`)
Decouples the logic from the physical device. This allows development on Windows while targeting Pi Zero.
- **`DisplayDriver` (ABC)**:
    - `draw_image(image: PIL.Image)`
    - **Implementations**: `PygameDisplay` (PC Window), `SSD1306Driver` (Pi OLED), `EInkDriver` (Pi Memory Display).
- **`InputDriver` (ABC)**:
    - `get_events()` -> returns list of abstract events (e.g., `BTN_UP`, `BTN_SELECT`, `KNOB_CW`).
    - **Implementations**: `KeyboardInput` (PC Arrow keys), `GPIOInput` (Pi physical buttons/rotary encoder).

### 3. Data Providers (`providers/`)
Modular system to fetch scores.
- **`SportsProvider` (ABC)**:
    - `get_live_matches()`
    - `get_match_detail(match_id)`
- **`CricketProvider`**: Scrapes Cricbuzz/ESPN (lite versions) or similar free sources.
- **`FootballProvider`**: (Future) scrapes Flashscore/LiveScore.
- **Data Model**: Normalized dictionaries (e.g., `{'team_a': 'IND', 'score_a': '150/2', ...}`).

### 4. UI Engine (`ui/`)
Responsible for converting "State" into pixels.
- **Technology**: Uses **Pillow (PIL)** to draw text and shapes onto a canvas. This is CPU efficient and translates perfectly to OLED/E-Ink displays.
- **`Renderer`**: Takes the current `State` and determines which "Scene" to draw.
- **`Layouts`**:
    - `ListView`: Vertical scrolling list of matches.
    - `DetailView`: Full screen single match.
    - `SplitView`: Top/Bottom split for monitoring two games.

## Folder Structure

```
SickFury/
├── main.py                # Entry point (auto-detects platform)
├── config.py              # Configuration (fonts, refresh rates, pin mappings)
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── app.py             # Main Loop
│   ├── state.py           # Data class for app state
│   └── events.py          # Event definitions
├── hal/
│   ├── __init__.py
│   ├── base.py            # Abstract Base Classes
│   ├── pc.py              # Pygame/Keyboard implementation
│   └── pi.py              # GPIO/OLED implementation
├── providers/
│   ├── __init__.py
│   ├── base.py            # Abstract Base Class for providers
│   └── cricket.py         # Cricket implementation
├── ui/
│   ├── __init__.py
│   ├── renderer.py        # Orchestrates drawing
│   ├── components.py      # Reusable UI bits (ScoreCard, StatusBar)
│   └── fonts/             # Bitmap fonts
└── utils/
    └── web.py             # Cached requests session, user-agent rotation
```

## Pi Zero Constraints & Design Choices

1.  **Pillow over Pygame for Rendering**:
    -   Pygame overhead is higher on headless Pi setups. Pillow allows us to manipulate a simple pixel buffer and send it directly to the SPI interface of a screen, which is much faster/lighter for the Zero.
    -   On PC, we just blit the Pillow image to a Pygame surface for visualization.

2.  **Threading vs Async**:
    -   We will use a separate **Thread** for data fetching. Network I/O on slow WiFi can block the UI.
    -   UI rendering runs on the main thread (easier integration with SPI libraries).
    -   We avoid full `asyncio` complexity unless necessary, standard `threading` is sufficient for simple background polling.

3.  **Memory Management**:
    -   Explicitly trigger garbage collection if memory climbs (rare for this scope).
    -   Avoid heavy browser engines (Selenium is banned). Use `requests` and lightweight HTML parsing.

4.  **Buttons/Knob Logic**:
    -   Debouncing logic handled in `GPIOInput` class.
    -   Map Rotary Encoder CW/CCW to Next/Prev events.
