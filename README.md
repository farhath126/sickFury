# SickFury Pager 📟

**"Motherf..." — Nick Fury (probably, if he saw this)**

SickFury is a retro-futuristic, handheld sports pager designed to deliver live scores straight to your pocket with zero fluff. Inspired by the iconic Captain Marvel pager, this device strips away the noise of modern betting apps and gives you just the raw data in a beautiful, low-fidelity 128x64 pixel interface.

Currently running as a PC simulation, SickFury is destined for the **Raspberry Pi Zero W**, where it will live as a dedicated hardware device.

---

## 🚀 Features

### Multi-Sport Support
SickFury doesn't discriminate. We track the biggest games across:
*   **🏏 Cricket**:  
    *   Live scores from top international and league matches.
    *   Real-time batsmen stats (runs, balls faced) for live games.
    *   Smart card parsing (Rich vs Compact views).
*   **⚽ Football**:  
    *   Coverage of **EPL, LaLiga, Bundesliga, Serie A, Ligue 1, and UCL**.
    *   **Live Match Clock**: Real-time minute tracking.
    *   **Goal Details**: See exactly who scored and when (Goals, Penalties, Own Goals).
    *   Smart sorting: Live games always float to the top.
*   **🔫 Counter-Strike 2 (CS2)**:  
    *   **Unified Feed**: Live, Upcoming, and Past matches all in one list.
    *   **Format Detection**: Automatically flags BO3/BO5 matches.
    *   **Map Parsing**: Scans match details for map picks (Mirage, Inferno, Nuke, etc.).
    *   Score breakdown for finished games.

### The "Pager" Aesthetic
*   **128x64 Resolution**: Every pixel counts. Optimized for small OLED displays.
*   **Menu System**: Simple list navigation to switch between sports.
*   **Physical Controls (Simulated)**: Controlled via keyboard (`UP`, `DOWN`, `ENTER`, `BACK`) to mimic tactile buttons.
*   **No API Keys**: Powered by custom-built reliable web scrapers (Cricbuzz, ESPN, GosuGamers). No paid subscriptions required.

---

## 🛠️ Architecture

SickFury is built to be **hackable** and **hardware-agnostic**.

*   **HAL (Hardware Abstraction Layer)**: The core logic has no idea what it's running on. 
    *   *PC Implementation*: Uses `pygame` to render the display and capture key presses.
    *   *Pi Implementation (Coming Soon)*: Will drop in to drive SPI OLEDs and read GPIO buttons directly.
*   **Provider System**: Each sport is a self-contained module. Want to add F1? Just write a new Provider class.
*   **State Machine**: robust event loop handling fetching, parsing, and rendering without blocking the UI.

---

## 🎮 How to Run (PC Simulation)

1.  **Install Dependencies**:
    ```bash
    pip install pygame requests beautifulsoup4
    ```

2.  **Launch the Pager**:
    ```bash
    python main.py
    ```

3.  **Controls**:
    *   `UP` / `DOWN`: Scroll lists or text.
    *   `ENTER`: Select sport / View match details.
    *   `ESC` / `BACK`: Go back to menu / previous screen.

---

## 🔮 Roadmap

*   **Hardware Build**: Porting to Raspberry Pi Zero W + 0.96" / 1.3" OLED.
*   **Battery Optimization**: Deep sleep modes for weeks of standby.
*   **More Sports**: F1, NBA, and maybe some eSports League of Legends.

---

*Built with ❤️ and a distinct lack of patience for ads.*
