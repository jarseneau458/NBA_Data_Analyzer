from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd


class PlayerAnalyzer:
    def __init__(self, full_name):
        """
         runs once when you create the object. It downloads the data
        and stores it in memory so all the other functions can use it instantly.
        """

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
        """ Calculates player averages
        Returns Averages plus last 10 and 5 games stats while hiding unnecesary colunms
        """
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

    def prop_line_analyzer(self, stat_category, prop_line):
        """Calculates the hit rate of a stat category based on the prop line."""
        #adds up the hit rates 
        season_hits_over = (self.df[stat_category] > prop_line).sum()
        season_hits_under = len(self.df) - season_hits_over
        l10_hits_over = (self.last_10[stat_category] > prop_line).sum()
        l10_hits_under = len(self.last_10) - l10_hits_over
        l5_hits_over = (self.last_5[stat_category] > prop_line).sum()
        l5_hits_under = len(self.last_5) - l5_hits_over

        season_over_rate = round((season_hits_over / len(self.df))* 100, 2)
        season_under_rate = 100 - season_over_rate

        l10_over_rate = round((l10_hits_over / 10)* 100, 2)
        l10_under_rate = 100 - l10_over_rate

        l5_over_rate = round((l5_hits_over / 5)* 100, 2)
        l5_under_rate = 100 - l5_over_rate

        return {
            "Stat Category": stat_category.Upper(),
            "Prop Line": prop_line,
            "Season Over Hits": season_hits_over,
            "Season Under Hits": season_hits_under,
            "Season Over Rate": season_over_rate,
            "Season Under Rate": season_under_rate,
            "Last 10 Over Hits": l10_hits_over,
            "Last 10 Under Hits": l10_hits_under,
            "Last 10 Over Rate": l10_over_rate,
            "Last 10 Under Rate": l10_under_rate,
            "Last 5 Over Hits": l5_hits_over,
            "Last 5 Under Hits": l5_hits_under,
            "Last 5 Over Rate": l5_over_rate,
            "Last 5 Under Rate": l5_under_rate
        }

















