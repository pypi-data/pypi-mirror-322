class SportsMappingDefaults:
    LEAGUE_MAPPING = {
        "cs": "CS2",
        "dota": "DOTA2",
        "val": "VAL",
        "cod": "COD",
        "lol": "LOL",
        "nba": "NBA",
        "fifa": "SOCCER",
        "basketball": "FPA",
    }

    @classmethod
    def get_league_mapping(cls, league):
        """
        Convert a league to its proper league name using the default mapping.
        :param league: League to check.
        :return: Returns the proper league name if it exists, otherwise the original league.
        """
        return cls.LEAGUE_MAPPING.get(league.lower(), league)
