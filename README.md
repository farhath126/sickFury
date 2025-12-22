SickFury Pager

“Motherf—” — Nick Fury, probably

SickFury is a retro-futuristic handheld sports pager that delivers live scores with zero noise. No ads, no betting junk, no endless scrolling — just the game.

Inspired by the Captain Marvel pager, it leans into old-school constraints: a tiny 128×64 pixel display showing only what matters. Right now it runs as a PC simulation, but the end goal is a dedicated Raspberry Pi Zero W device that lives as standalone hardware.

What it does
Multi-sport support

Cricket

Live scores from major international and league matches

Current batsmen stats (runs, balls faced)

Automatically switches between compact and detailed views depending on the match

Football

Covers EPL, LaLiga, Bundesliga, Serie A, Ligue 1, and UCL

Live match clock that updates in real time

Goal details (scorer, minute, penalty or own goal)

Live matches always stay at the top

Counter-Strike 2

Unified list for live, upcoming, and completed matches

BO3 / BO5 detection

Map information parsed from match details

Clear score breakdown for finished games

The pager idea

This project is intentionally constrained.

128×64 resolution forces clarity

Simple list-based menus

Button-driven navigation (simulated via keyboard for now)

No API keys or subscriptions — data is scraped from public sources

The goal is for it to feel like hardware, not a mobile app in disguise.

How it’s built

SickFury is modular and hardware-agnostic by design.

Hardware Abstraction Layer
Core logic is independent of the platform.

PC version uses pygame

Raspberry Pi version will directly drive OLEDs and GPIO buttons

Provider system
Each sport is its own module. Adding a new sport is just writing a new provider.

State-driven loop
Fetching, parsing, and rendering are handled without blocking the UI.

Running it on PC

Install dependencies:

pip install pygame requests beautifulsoup4


Run:

python main.py


Controls:

UP / DOWN: scroll

ENTER: select or open match

ESC / BACK: return

Roadmap

Port to Raspberry Pi Zero W with a small OLED

Battery optimization for long standby time

Additional sports such as F1 and NBA

Built with care, curiosity, and a strong dislike for ads.