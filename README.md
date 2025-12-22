# SickFury Pager

A retro-style, handheld sports ticker device inspired by Nick Fury's pager.

## Goals
- **Phase 1**: PC-based simulation for development and testing.
- **Phase 2**: Raspberry Pi Zero deployment with OLED/E-Ink display and physical buttons.

## Features
- Live sports scores (Cricket first).
- Support for dual-game monitoring.
- Modular plugin system for data providers.
- "Terminal-like" low-res UI.

## Architecture
- **HAL (Hardware Abstraction Layer)**: Decouples logic from hardware. Supports PC (Pygame) and Pi (GPIO/SPI).
- **Providers**: Independent modules for fetching statistics (free APIs/scraping).
- **Core**: Event-driven architecture loop.

## Setup (Phase 1)
1. Install dependencies: `pip install -r requirements.txt`
2. Run simulation: `python main.py`
