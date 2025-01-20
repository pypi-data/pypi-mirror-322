from DFS_Wrapper.DFS_Base import DFS
from DFS_Wrapper.default_mapper import SportsMappingDefaults

class Underdog(DFS):
    # Mapping Index for _map_team_opponent due to different sports having different formats.
    OTHER_MAPPING_TEAM_INDEX = ("MASL", "ESPORTS", "UNRIVALED", "VAL", "CS", "LOL", "DOTA")

    def __init__(self):
        super().__init__()
        self.stats_cache = {}

    def _get_underdog_data_(self):
        """
        Get Underdog Data
        :return: Returns the Underdog Data
        """
        return self._get_player_information()

    def _get_player_information(self):
        """
        Gets all player information.
        :return: Returns the player information in a list of dictionaries.
        """
        player_info = []

        for player in self.api_data["players"]:
            for match in self.api_data["appearances"]:
                if player.get("id") != match.get("player_id"):
                    continue

                player_info.append({
                    "player_id": player.get("id"),
                    "player_name": self._fix_name(player.get("first_name"), player.get("last_name")),
                    "sport_id": player.get("sport_id") if player.get("sport_id") != "ESPORTS" else self._fix_sport_id(player.get("first_name")),
                    "match_id": match.get("match_id"),
                    "match_type": match.get("match_type"),
                    "team_id": match.get("team_id"),
                    "stat_id": match.get("id"),
                    **self._get_team_details(match.get("match_id"), match.get("team_id"))[0],
                    "stats": self._get_stats(match.get("id")),
                })

        return player_info

    def _fix_sport_id(self, first_name):
        return first_name.replace(":", "").strip()



    def _get_team_details(self, match_id, team_id):
        """
        Get Team Details
        :param match_id: Match ID
        :param team_id: Team ID
        :return: Returns the team details.
        """
        solo_game = self._solo_game(match_id)
        if solo_game:
            return solo_game

        return [
            {
                "game_date_time": game.get("scheduled_at"),
                **{key: value for key, value in self._map_team_opponent(team_id, game).items()},
            }

            for game in self.api_data["games"]
            if game.get("id") == match_id
        ]

    def _get_stats(self, stat_id):
        """
        Get Stats
        :param stat_id: Stat ID of player.
        :return: Returns the stats for the player.
        """
        if not self.stats_cache and self.api_data:
            for stat in self.api_data["over_under_lines"]:
                appearance_id = stat.get("over_under").get("appearance_stat").get("appearance_id")
                if appearance_id not in self.stats_cache:
                    self.stats_cache[appearance_id] = []
                self.stats_cache[appearance_id].append({
                    "stat_type": stat.get("over_under").get("appearance_stat").get("display_stat").strip(),
                    "line_value": float(stat.get("stat_value")),
                    "over_multiplier": self.get_multiplier(stat, over=True),
                    "under_multiplier": self.get_multiplier(stat)
                })

        return self.stats_cache.get(stat_id, [])


    def get_multiplier(self, stat_details, over=False):
        """
        Get the multiplier for the player
        :param stat_details: Pass in the stat details dictionary.
        :param over: Set to True if wanting the over multiplier, False for the under multiplier.
        :return: Returns the multiplier for the player.
        """
        for option in stat_details["options"]:
            if option.get("choice_display") == "Higher" and over:
                return float(option.get("payout_multiplier"))
            elif option.get("choice_display") != "Higher" and not over:
                return float(option.get("payout_multiplier"))


    def _map_team_opponent(self, team_id, game):
        """
        Map Team Opponent. Keep in mind different sports have different formats for team/opponent.
        :param team_id: Team ID
        :param game: Game Instance
        :return: Returns the team and opponent.
        """
        if game.get("sport_id") in self.OTHER_MAPPING_TEAM_INDEX:
            match_title = self._fix_title(game.get("title"))
            if team_id == game.get("home_team_id"):
                return {
                    "team": match_title.replace(".", "").split("vs")[1].strip(),
                    "opponent": match_title.replace(".", "").split("vs")[0].strip()
                }
            elif team_id == game.get("away_team_id"):
                return {
                    "team": match_title.replace(".", "").split("vs")[0].strip(),
                    "opponent": match_title.replace(".", "").split("vs")[1].strip()
                }

        if team_id == game.get("home_team_id"):
            return {
                "team": game["title"].split("@")[1].strip() if "@" in game["title"] else game["title"].replace(".", "").split("vs")[0].strip(),
                "opponent": game["title"].split("@")[0].strip() if "@" in game["title"] else game["title"].replace(".", "").split("vs")[1].strip(),
            }
        elif team_id == game.get("away_team_id"):
            return {
                "team": game["title"].split("@")[0].strip() if "@" in game["title"] else game["title"].replace(".","").split("vs")[1].strip(),
                "opponent": game["title"].split("@")[1].strip() if "@" in game["title"] else game["title"].replace(".", "").split("vs")[0].strip(),
            }

        return {}

    def _fix_title(self, match_title):
        """
        Fix the title of the match.
        :param match_title: Match Title
        :return: Fixed matches.
        """
        if ":" in match_title:
            return match_title.split(":")[1].strip()
        return match_title

    def _solo_game(self, match_id):
        """
        Get Solo Game
        :param match_id: Match ID
        :return: Returns the solo game details.
        """
        return [
            {
                "game_date_time": solo_game.get("scheduled_at"),
                "match": solo_game.get("title"),

            }
            for solo_game in self.api_data.get("solo_games")
            if solo_game.get("id") == match_id
        ]


    def _fix_name(self, first_name, last_name):
        """
        Fixes the players name, as Esports don't have first name.
        :param first_name: API First Name.
        :param last_name: API Last Name
        :return: Returns the players name.
        """
        if first_name is None or ":" in first_name or first_name == "":
            return last_name.strip()
        return f"{first_name} {last_name}"

    def _organize_data(self, underdog_data):
        """
        Organize the data by league
        :param underdog_data: Underdog Data
        :return: Returns  a dictionary of data organized by league.
        """
        organized = {}

        for data in underdog_data:
            league = SportsMappingDefaults.get_league_mapping(data.get("sport_id"))

            base_entry = {
                "player_name": data.get("player_name"),
                "player_id": data.get("player_id"),
                "match_id": data.get("match_id"),
                "match_type": data.get("match_type"),
                "team_id": data.get("team_id"),
                "stat_id": data.get("stat_id"),
                "game_date_time": data.get("game_date_time"),
            }

            if "team" in data and "opponent" in data:
                base_entry.update({
                    "team": data.get("team"),
                    "opponent": data.get("opponent")
                })
            elif "match" in data:
                base_entry["match"] = data.get("match")

            base_entry.update({"stats": data.get("stats")})

            if league not in organized:
                organized[league] = []
            organized[league].append(base_entry)

        return organized


    def get_data(self, organized_data=True):
        """
        Get the Underdog API Data.
        :return: Returns the Underdog API data in a list of dictionaries if organize_data is False,
        else returns a dictionary of data organized by league.
        """
        self.api_data = self._get_api_data('underdog')
        underdog_data = self._get_player_information()
        return self._organize_data(underdog_data) if organized_data else underdog_data


    def _get_leagues_(self):
        """
        Get Leagues
        :return: Returns the League in a set.
        """
        self.api_data = self._get_api_data('underdog')

        return set(
            SportsMappingDefaults.get_league_mapping(league["sport_id"])
            for league in self.api_data["players"] if league.get("sport_id") is not None
        )

    def get_leagues(self, organized_data=True):
        """
        Get Leagues
        :return: Returns leagues in a set.
        """
        return self._get_leagues_()

