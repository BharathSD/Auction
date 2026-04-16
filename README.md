# Auction App (Tkinter)

A desktop player-auction application built with Python, Tkinter, and Excel-backed data.

## What This App Does

- Loads players from an Excel sheet.
- Filters players by availability.
- Displays player profile (name, ratings, image).
- Runs bid increments by team.
- Tracks team budget and selected players.
- Supports saving/loading pre-auction state.

## Tech Stack

- Python 3.12+
- Tkinter (GUI)
- pandas + openpyxl (Excel IO)
- Pillow (images)

## Project Files

- main entry: mainFile.py
- player/data model: player.py
- table UI: playerTable.py
- config: AuctionConfig.json
- dependencies: requirements.txt
- sample input template: PlayerData_Template.xlsx

## Setup

### 1) Create and activate virtual environment (optional but recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3) Run the app

```powershell
python mainFile.py
```

## Configuration

All runtime configuration is in AuctionConfig.json.

Current keys:

- player_data_file: source Excel file for players.
- auctioned_players_file: output/load file for saved auction state.
- availability_column: availability column name in player_data_file.
- max_players_per_captain: default roster size for each captain.
- initial_budget_per_captain: default starting budget.
- images_folder: folder containing player photos.
- captains: list of captain names, or objects for per-captain overrides.

### Captains format

Simple list:

```json
{
  "captains": ["Anoop", "Shashi"]
}
```

Per-captain overrides:

```json
{
  "max_players_per_captain": 8,
  "initial_budget_per_captain": 150000,
  "captains": [
    { "name": "Anoop", "max_players": 10, "initial_budget": 200000 },
    { "name": "Shashi" }
  ]
}
```

## Player Excel Requirements

The app validates required columns at startup.

Required columns in player_data_file:

- UID
- Photo
- Name
- Gender
- Bowl_rating
- Bat_rating
- Availbale

Note: the configured default spelling is Availbale because current data/code use that exact header.

Optional metadata columns may exist and are ignored if present:

- ID
- Start time
- Completion time
- Email
- Last modified time
- Name2
- Extracted uid
- Are the Uid's Same
- Reporting Manager
- Mobile No

Use PlayerData_Template.xlsx as a starter template.

## Images

- Player images are loaded from images_folder using the file name parsed from the Photo URL/path.
- Missing player images no longer crash the app; a placeholder image is shown.
- The startup poster is optional. If not configured, a placeholder image is shown.

## Save/Load Pre-Auction Data

- Click Load Pre Auction to restore previously saved auctioned players from auctioned_players_file.
- App saves auction state when SOLD actions are applied.

## Troubleshooting

- ModuleNotFoundError: install dependencies with requirements.txt.
- Missing required columns error: verify player_data_file headers match config.
- Missing configuration file: ensure AuctionConfig.json exists at project root.
- Image missing: place image files under images_folder with matching file names.

## Notes

- __pycache__/ and .venv/ are ignored by .gitignore.
- AuctionedPlayers.xlsx is runtime data; commit only if intentionally versioning state.
