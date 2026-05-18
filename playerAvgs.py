from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd


class PlayerAnalyzer:
    def __init__(self, full_name):
        """
         runs once when you create the object. It downloads the data
        and stores it in memory so all the other functions can use it instantly.
        """
        print(f"\n[System] Fetching data for {full_name}...")
        self.full_name = full_name
        self.player_id = players.find_players_by_full_name(full_name)[0]['id']


        log = playergamelog.PlayerGameLog(self.player_id, season='2025-26')
        self.df = log.get_data_frames()[0]


        self.last_10 = self.df.head(10)
        self.last_5 = self.df.head(5)
        self.stats_tracked = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
                              'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

        self.hidden_columns = ['SEASON_ID', 'PLAYER_ID', 'Player_ID', 'GAME_ID', 'Game_ID', 'VIDEO_AVAILABLE']

    def get_trends(self):
        """ Calculates player averages """
        season_avgs = self.df[self.stats_tracked].mean().round(1).to_dict()
        last_10_avgs = self.last_10[self.stats_tracked].mean().round(1).to_dict()
        last_5_avgs = self.last_5[self.stats_tracked].mean().round(1).to_dict()

        return {
            "Season Averages": season_avgs,
            "Last 10 Averages": last_10_avgs,
            "Last 10 Games": self.last_10.drop(columns=self.hidden_columns, errors='ignore'),
            "Last 5 Averages": last_5_avgs,
            "Last 5 Games": self.last_5.drop(columns=self.hidden_columns, errors='ignore')
        }













