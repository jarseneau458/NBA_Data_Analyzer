from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

from BaseAnalyzer import BaseAnalyzer


class PlayerAnalyzer(BaseAnalyzer):
    def __init__(self, full_name, season='2025-26', season_type='Regular Season'):
        """
        Downloads the data from the NBA API.
        Analyzes the player's season game logs and last 10 and 5 games.
        """

        super().__init__()
        self.full_name = full_name
        self.player_id = players.find_players_by_full_name(full_name)[0]['id']
        #season_id = get_season_id(season, season_type)


        #gets player from nba_api

        log = playergamelog.PlayerGameLog(self.player_id, season=season, season_type_all_star=season_type)
        self.df = log.get_data_frames()[0]


        self.last_10 = self.df.head(10)
        self.last_5 = self.df.head(5)
        self.stats_tracked = ['PTS', 'AST' ,'REB','OREB', 'DREB' , 'STL', 'BLK','MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA','TOV', 'PF' ]

        self.hidden_columns = ['SEASON_ID', 'PLAYER_ID', 'GAME_ID', 'VIDEO_AVAILABLE']

    def get_trends(self):
        """ Calculates player averages
        Returns Averages plus last 10 and 5 games stats while hiding unnecesary colunms
        """
        season_avgs = self.df[self.stats_tracked].mean().round(1).to_dict()
        last_10_avgs = self.last_10[self.stats_tracked].mean().round(1).to_dict()
        last_5_avgs = self.last_5[self.stats_tracked].mean().round(1).to_dict()

        return {
            "Season Averages": season_avgs,

            "Last 10 Games": self.last_10.drop(columns=self.hidden_columns, errors='ignore', index = False),
            "Last 10 Averages": last_10_avgs,

            "Last 5 Games": self.last_5.drop(columns=self.hidden_columns, errors='ignore', index=False),
            "Last 5 Averages": last_5_avgs
        }

    def get_simplifed_averages(self):
        """ Calculates player averages
        Returns Averages plus last 10 and 5 games stats while hiding unnecesary colunms"""

        essential_stats = ['PTS', 'AST', 'REB', 'BLK', 'STL']
        season_avgs = self.df[essential_stats].mean().round(1).to_dict()
        last_10_avgs = self.last_10[essential_stats].mean().round(1).to_dict()
        last_5_avgs = self.last_5[essential_stats].mean().round(1).to_dict()

        return {
            "Season Averages": season_avgs,
            "Last 10 Averages": last_10_avgs,
            "Last 5 Averages": last_5_avgs
        }












if __name__ == "__main__":
    player = PlayerAnalyzer("Jaylen Brown")
    player.calculate_projections("PTS", "LA Clippers")
    print(player.calculate_projections("PTS", "LA Clippers"))















