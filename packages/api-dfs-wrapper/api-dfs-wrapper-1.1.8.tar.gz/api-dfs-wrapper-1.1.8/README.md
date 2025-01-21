# DFS Wrapper
A simple Python wrapper for DFS Books API to fetch player stats, leagues, and other game data.

## Installation
Install the package directly from PyPI:
pip install api-dfs-wrapper

## Usage

### Import PrizePick wrapper
from DFS_Wrapper import PrizePick

### Import Underdog Wrapper
from DFS_Wrapper import Underdog

### Initialize PrizePick wrapper
prizepick = PrizePick()

### Initialize Underdog wrapper
underdog = Underdog()

### Get PrizePick data
pp_data = prizepick.get_data()

### Get Underdog data
ud_data = underdog.get_data()

### Get PrizePick Leagues
pp_leagues = prizepick.get_leagues()

### Get Underdog Leagues
ud_leagues = underdog.get_leagues()


### Methods
get_data(organize_data): Fetches PrizePick data. If organize_data is set to true, 
this will return a dictionary of leagues with key being the league name. organize_data is defaulted to true.
If organize_data is false, will return a list of all data, non-organized.

get_leagues(): Returns a dictionary of leagues with their IDs. [PrizePick Only]

get_leagues(): Returns a set of leagues [Underdog Only]

### Example JSON Return for Prizepicks [Non-Organized]
```json
[
    {
        "player_id": "225032",
        "player_name": "Danielle Hunter",
        "is_live": false,
        "league": "NFL1H",
        "league_id": "35",
        "odds_type": "standard",
        "stat_type": "Sacks",
        "status": "pre_game",
        "team": "HOU",
        "opponent": "KC",
        "line_score": 0.13,
        "start_time": "2025-01-18T16:30:00-05:00"
    },
    {
        "player_id": "211159",
        "player_name": "Ka'imi Fairbairn",
        "is_live": false,
        "league": "NFL",
        "league_id": "9",
        "odds_type": "demon",
        "stat_type": "FG Made",
        "status": "pre_game",
        "team": "HOU",
        "opponent": "KC",
        "line_score": 2.5,
        "start_time": "2025-01-18T16:30:00-05:00"
    }
]
```
### Example JSON Return for Underdog [Non-Organized]
```
[
    {
        "player_name": "LaMelo Ball",
        "player_id": "b78ba991-272a-438e-81d6-901d66c7e09a",
        "sport_id": "NBA",
        "match_id": 85801,
        "match_type": "Game",
        "team_id": "11cfe154-8ba6-4c22-be8f-2365656fb4da",
        "stat_id": "872f2308-db67-41e8-95f0-1c20d4061b1b",
        "team": "CHA",
        "opponent": "CHI",
        "stats": [
            {
                "stat_type": "Points",
                "line_value": 30.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "Pts + Rebs + Asts",
                "line_value": 45.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "1Q Points",
                "line_value": 7.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "Assists",
                "line_value": 8.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "Rebounds",
                "line_value": 5.5,
                "over_multiplier": 0.92,
                "under_multiplier": 1.07
            },
            {
                "stat_type": "1Q Pts + Rebs + Asts",
                "line_value": 12.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "Pts+Reb+Ast in First 5 Min.",
                "line_value": 6.5,
                "over_multiplier": 1.04,
                "under_multiplier": 0.93
            },
            {
                "stat_type": "Points in First 5 Min.",
                "line_value": 4.5,
                "over_multiplier": 1.07,
                "under_multiplier": 0.91
            },
            {
                "stat_type": "Rebounds + Assists",
                "line_value": 14.5,
                "over_multiplier": 1.04,
                "under_multiplier": 0.94
            },
            {
                "stat_type": "1Q Rebounds",
                "line_value": 1.5,
                "over_multiplier": 1.05,
                "under_multiplier": 0.93
            },
            {
                "stat_type": "3-Pointers Made",
                "line_value": 4.5,
                "over_multiplier": 0.87,
                "under_multiplier": 1.12
            },
            {
                "stat_type": "1Q Assists",
                "line_value": 2.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "Points + Rebounds",
                "line_value": 36.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "Assists in First 5 min.",
                "line_value": 1.5,
                "over_multiplier": 1.62,
                "under_multiplier": 0.69
            },
            {
                "stat_type": "Points + Assists",
                "line_value": 39.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "Double Doubles",
                "line_value": 0.5,
                "over_multiplier": 1.15,
                "under_multiplier": 0.85
            },
            {
                "stat_type": "1Q 3-Pointers Made",
                "line_value": 0.5,
                "over_multiplier": null,
                "under_multiplier": 2.14
            },
            {
                "stat_type": "Steals",
                "line_value": 1.5,
                "over_multiplier": 1.16,
                "under_multiplier": 0.83
            },
            {
                "stat_type": "1H Pts + Rebs + Asts",
                "line_value": 23.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "1H Assists",
                "line_value": 4.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "1H Points",
                "line_value": 16.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "1H 3-Pointers Made",
                "line_value": 2.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "Fantasy Points",
                "line_value": 52.45,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "FT Made",
                "line_value": 5.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            },
            {
                "stat_type": "Turnovers",
                "line_value": 3.5,
                "over_multiplier": 1,
                "under_multiplier": 1
            }
        ]
    },
]
```
### Example JSON Return for Prizepicks [Organized]
```
{
 "NFL": [
        {
            "player_id": "224099",
            "player_name": "Will Anderson",
            "team": "HOU",
            "opponent": "KC",
            "stats": [
                {
                    "stat_type": "Sacks",
                    "line_score": 0.25,
                    "odds_type": "standard",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Sacks",
                    "line_score": 1.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                }
            ]
        },
        {
            "player_id": "206322",
            "player_name": "Joe Mixon",
            "team": "HOU",
            "opponent": "KC",
            "stats": [
                {
                    "stat_type": "Rush Yards",
                    "line_score": 54.5,
                    "odds_type": "standard",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush Yards in First 5 Attempts",
                    "line_score": 17.5,
                    "odds_type": "standard",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Fantasy Score",
                    "line_score": 12.5,
                    "odds_type": "standard",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush+Rec Yds",
                    "line_score": 77.5,
                    "odds_type": "standard",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush Attempts",
                    "line_score": 15.5,
                    "odds_type": "standard",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Longest Reception",
                    "line_score": 9.5,
                    "odds_type": "standard",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Receiving Yards",
                    "line_score": 16.5,
                    "odds_type": "standard",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush+Rec TDs",
                    "line_score": 0.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Longest Rush",
                    "line_score": 13.5,
                    "odds_type": "standard",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Receptions",
                    "line_score": 2.5,
                    "odds_type": "goblin",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Receptions",
                    "line_score": 3.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Receptions",
                    "line_score": 4.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rec Targets",
                    "line_score": 3.5,
                    "odds_type": "standard",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Receiving Yards",
                    "line_score": 29.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush Yards",
                    "line_score": 79.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Receiving Yards",
                    "line_score": 39.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush+Rec Yds",
                    "line_score": 109.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush+Rec Yds",
                    "line_score": 99.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush+Rec Yds",
                    "line_score": 59.5,
                    "odds_type": "goblin",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush Yards",
                    "line_score": 89.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush Yards",
                    "line_score": 74.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush Yards",
                    "line_score": 69.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush Yards",
                    "line_score": 39.5,
                    "odds_type": "goblin",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush Yards",
                    "line_score": 49.5,
                    "odds_type": "goblin",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                },
                {
                    "stat_type": "Rush+Rec Yds",
                    "line_score": 89.5,
                    "odds_type": "demon",
                    "start_time": "2025-01-18T16:30:00-05:00",
                    "status": "pre_game"
                }
            ]
        },
 }
```
### Example JSON Return for Underdog [Organized]
```
{
    "NFL": [
        {
            "player_name": "Patrick Mahomes",
            "player_id": "f1766f00-503b-4b13-a5d1-cd4347423121",
            "team": "KC",
            "opponent": "HOU",
            "match_id": 104858,
            "match_type": "Game",
            "team_id": "a6f458f4-5078-56e4-a839-af96f1191314",
            "stat_id": "4c28ae8e-873c-45b0-a62d-1b737d630280",
            "stats": [
                {
                    "stat_type": "Passing Yards",
                    "line_value": 254.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Passing TDs",
                    "line_value": 1.5,
                    "over_multiplier": 0.77,
                    "under_multiplier": 1.32
                },
                {
                    "stat_type": "Rush + Rec TDs",
                    "line_value": 0.5,
                    "over_multiplier": 2.67,
                    "under_multiplier": null
                },
                {
                    "stat_type": "Pass + Rush Yards",
                    "line_value": 281.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Passing Attempts",
                    "line_value": 37.5,
                    "over_multiplier": 1.04,
                    "under_multiplier": 0.94
                },
                {
                    "stat_type": "Rushing Yards",
                    "line_value": 23.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Completions",
                    "line_value": 25.5,
                    "over_multiplier": 1.04,
                    "under_multiplier": 0.94
                },
                {
                    "stat_type": "Interceptions",
                    "line_value": 0.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Rushing Attempts",
                    "line_value": 4.5,
                    "over_multiplier": 1.06,
                    "under_multiplier": 0.93
                },
                {
                    "stat_type": "Longest Rush",
                    "line_value": 12.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "1H Rushing Yards",
                    "line_value": 9.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "1H Rush + Rec TD",
                    "line_value": 0.5,
                    "over_multiplier": 5.65,
                    "under_multiplier": null
                },
                {
                    "stat_type": "1Q Passing TDs",
                    "line_value": 0.5,
                    "over_multiplier": 1.36,
                    "under_multiplier": 0.76
                },
                {
                    "stat_type": "1Q Passing Yards",
                    "line_value": 58.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "1H Passing Yards",
                    "line_value": 132.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "1H Passing TDs",
                    "line_value": 0.5,
                    "over_multiplier": 0.75,
                    "under_multiplier": 1.38
                },
                {
                    "stat_type": "Team First TD Scorer",
                    "line_value": 0.5,
                    "over_multiplier": null,
                    "under_multiplier": 5.94
                },
                {
                    "stat_type": "Longest Completion",
                    "line_value": 35.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "First TD Scorer",
                    "line_value": 0.5,
                    "over_multiplier": null,
                    "under_multiplier": 11.59
                },
                {
                    "stat_type": "1Q Rushing Yards",
                    "line_value": 0.5,
                    "over_multiplier": 1.04,
                    "under_multiplier": 0.94
                },
                {
                    "stat_type": "1Q Rush + Rec TDs",
                    "line_value": 0.5,
                    "over_multiplier": 13.51,
                    "under_multiplier": null
                },
                {
                    "stat_type": "Fantasy Points",
                    "line_value": 20.55,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Sacks Taken",
                    "line_value": 2,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Fumbles Lost",
                    "line_value": 0.5,
                    "over_multiplier": 2.54,
                    "under_multiplier": null
                },
                {
                    "stat_type": "Game High Pass Yards",
                    "line_value": 0.5,
                    "over_multiplier": null,
                    "under_multiplier": 0.85
                },
                {
                    "stat_type": "Game High Rush Yards",
                    "line_value": 0.5,
                    "over_multiplier": null,
                    "under_multiplier": 6.22
                }
            ]
        },
        {
            "player_name": "C.J. Stroud",
            "player_id": "59614625-f243-4cb9-8038-146619f12e70",
            "team": "HOU",
            "opponent": "KC",
            "match_id": 104858,
            "match_type": "Game",
            "team_id": "4ab08caa-b79d-598e-82ef-0906a60d2a89",
            "stat_id": "b0778e0c-c05d-4b9f-b0db-8fc05e2ee855",
            "stats": [
                {
                    "stat_type": "Passing Yards",
                    "line_value": 225.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Passing TDs",
                    "line_value": 1.5,
                    "over_multiplier": 1.42,
                    "under_multiplier": 0.74
                },
                {
                    "stat_type": "Pass + Rush Yards",
                    "line_value": 243.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Rush + Rec TDs",
                    "line_value": 0.5,
                    "over_multiplier": 2.94,
                    "under_multiplier": null
                },
                {
                    "stat_type": "Passing Attempts",
                    "line_value": 34.5,
                    "over_multiplier": 0.94,
                    "under_multiplier": 1.04
                },
                {
                    "stat_type": "Completions",
                    "line_value": 20.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Rushing Yards",
                    "line_value": 15.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Rushing Attempts",
                    "line_value": 3.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Interceptions",
                    "line_value": 0.5,
                    "over_multiplier": 0.81,
                    "under_multiplier": 1.21
                },
                {
                    "stat_type": "1H Passing TDs",
                    "line_value": 0.5,
                    "over_multiplier": 1.11,
                    "under_multiplier": 0.88
                },
                {
                    "stat_type": "Longest Completion",
                    "line_value": 35.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Longest Rush",
                    "line_value": 8.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "1H Rushing Yards",
                    "line_value": 5.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "1Q Rushing Yards",
                    "line_value": 0.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "1H Rush + Rec TD",
                    "line_value": 0.5,
                    "over_multiplier": 6.11,
                    "under_multiplier": null
                },
                {
                    "stat_type": "1Q Rush + Rec TDs",
                    "line_value": 0.5,
                    "over_multiplier": 13.24,
                    "under_multiplier": null
                },
                {
                    "stat_type": "1Q Passing TDs",
                    "line_value": 0.5,
                    "over_multiplier": 2.37,
                    "under_multiplier": null
                },
                {
                    "stat_type": "Fantasy Points",
                    "line_value": 15.65,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "First TD Scorer",
                    "line_value": 0.5,
                    "over_multiplier": null,
                    "under_multiplier": 12.29
                },
                {
                    "stat_type": "1Q Passing Yards",
                    "line_value": 44.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "1H Passing Yards",
                    "line_value": 104.5,
                    "over_multiplier": 1,
                    "under_multiplier": 1
                },
                {
                    "stat_type": "Fumbles Lost",
                    "line_value": 0.5,
                    "over_multiplier": 1.5,
                    "under_multiplier": 0.72
                },
                {
                    "stat_type": "Game High Pass Yards",
                    "line_value": 0.5,
                    "over_multiplier": null,
                    "under_multiplier": 1.14
                }
            ]
        },
}        

```

### Error Handling
Raises a custom RateLimit exception on status code 429 (rate-limited).

General exceptions for other API errors.

### Dependencies
requests: For making API calls.