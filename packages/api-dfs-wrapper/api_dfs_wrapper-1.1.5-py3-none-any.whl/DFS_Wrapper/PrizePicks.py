import json
from datetime import datetime
from DFS_Wrapper.DFS_Base import DFS
import pytz

class PrizePick(DFS):
    def __init__(self):
        super().__init__()

    def _get_prizepick_data(self):
        """
        Get PrizePick Data
        :return: PrizePick Data
        """
        player_info_map = {
            player["id"]: player
            for player in self.api_data["included"]
            if player.get("attributes") and player["attributes"].get("display_name")
        }

        def get_player_info(player_id):
            return player_info_map.get(player_id, {})

        return [
            {
                "player_id": game_details["relationships"]["new_player"]["data"]["id"],
                "player_name": get_player_info(game_details["relationships"]["new_player"]["data"]["id"]).get(
                    "attributes", {}).get("display_name"),
                "is_live": game_details["attributes"]["is_live"],
                "league": get_player_info(game_details["relationships"]["new_player"]["data"]["id"]).get(
                    "attributes", {}).get("league"),
                "league_id": get_player_info(game_details["relationships"]["new_player"]["data"]["id"]).get(
                    "relationships", {}).get("league", {}).get("data", {}).get("id"),
                "odds_type": game_details["attributes"]["odds_type"],
                "stat_type": game_details["attributes"]["stat_type"],
                "status": game_details["attributes"]["status"],
                "team": get_player_info(game_details["relationships"]["new_player"]["data"]["id"]).get(
                    "attributes", {}).get("team"),
                "opponent": game_details["attributes"]["description"].split(" ")[0],
                **(
                    {
                        "promo_line": game_details["attributes"].get("flash_sale_line_score"),
                        "discount_name": game_details["attributes"].get("discount_name"),
                        "discount_percentage": game_details["attributes"].get("discount_percentage"),
                        "end_promo_date": game_details["attributes"].get("end_time"),
                    }
                    if game_details["attributes"].get("flash_sale_line_score") else {
                        "line_value": game_details["attributes"]["line_score"],
                    }
                ),
                "game_date_time": self._convert_time(game_details["attributes"]["start_time"]),
            }
            for game_details in self.api_data["data"]
        ]

    def _organize_data(self, prizepick_data):
        """
        Organize PrizePick data by league
        :param prizepick_data: PrizePick Data
        :return: Returns a dictionary of PrizePick data organized by league.
        """
        organized_data = {}

        for data in prizepick_data:
            league = data["league"]

            if league not in organized_data:
                organized_data[league] = []

            player_entry = next(
                (player for player in organized_data[league] if player["player_id"] == data["player_id"] and player["opponent"] == data["opponent"]),
                None
            )

            if not player_entry:
                player_entry = {
                    "player_id": data["player_id"],
                    "player_name": data["player_name"],
                    "team": data["team"],
                    "opponent": data["opponent"],
                    "game_date_time": data["game_date_time"],
                    "stats": []
                }
                organized_data[league].append(player_entry)

            player_entry["stats"].append({
                "stat_type": data["stat_type"],
                **(
                    {
                        "promo_line": data.get("promo_line"),
                        "discount_name": data.get("discount_name"),
                        "discount_percentage": data.get("discount_percentage"),
                        "end_promo_date": data.get("end_time"),
                    }
                    if data.get("promo_line") else {
                        "line_value": data["line_value"],
                    }
                ),
                "odds_type": data["odds_type"],
                "status": data["status"]
            })

        return organized_data

    def _convert_time(self, date_str):
        """
        Convert the date to UTC format
        :param date_str: Pass in the date/time string
        :return: Returns the date/time in UTC format
        """
        prizepick_time = datetime.fromisoformat(date_str)
        utc_time = prizepick_time.astimezone(pytz.utc)
        return utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")


    def get_data(self, organize_data=True):
        """
        Get PrizePick Data
        :param organize_data: Organize the data by league
        :return: Returns a list of PrizePick data if organize_data is False, else returns dictionary of data organized by league.
        """
        self.api_data = self._get_api_data('prizepick')
        prizepick_data = self._get_prizepick_data()

        if not organize_data:
            return prizepick_data

        return self._organize_data(prizepick_data)

    def _get_leagues_(self):
        """
        Get Leagues / League ID
        :return: League Name : League ID
        """
        self.api_data = self._get_api_data('prizepick')

        return {
            league["attributes"]["league"]: league["relationships"]["league"]["data"]["id"]
            for league in self.api_data["included"] if
            league.get("attributes") and league["attributes"].get("league") is not None
        }

    def get_leagues(self):
        """
        Get Leagues
        :return: Returns the League Name: League ID
        """
        return self._get_leagues_()


if __name__ == "__main__":
    pp = PrizePick()
    with open("prizepick.json", "w") as f:
        json.dump(pp.get_data(), f)