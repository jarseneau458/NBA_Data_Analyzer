from nba_api.stats.static import teams
import pandas as pd
from nba_api.stats.static.teams import find_teams_by_full_name
from nba_api.stats.endpoints import TeamDashboardByGeneralSplits
from nba_api.stats.endpoints import teamgamelog


class TeamAnalyzer:
    def __init__(self, team_name, season, season_type):
        self.team_name = team_name
        self.team_id = find_teams_by_full_name(team_name)[0]['id']
        self.season = season
        self.season_type = season_type
        self.team_record_list = ['W', 'L']
        self.team_stats_list= [ 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'TOV', 'PLUS_MINUS']
        self.advanced_team_stats_list = ['OFF_RATING', 'DEF_RATING']


    def get_team_stats(self):

        team_stats = TeamDashboardByGeneralSplits(team_id=self.team_id, season=self.season, season_type_all_star=self.season_type).get_data_frames()[0]
        team_record = team_stats[self.team_record_list]

        team_stats_df = team_stats[self.team_stats_list]
        advanced_team_stats =TeamDashboardByGeneralSplits(team_id=self.team_id, season=self.season, season_type_all_star=self.season_type, measure_type_detailed_defense='Advanced').get_data_frames()[0]
        advanced_team_stats_df = advanced_team_stats[self.advanced_team_stats_list]
        pts_allowed = (team_stats_df['PTS'] - team_stats_df['PLUS_MINUS'])[0]
        team_stats_df['PTS_ALLOWED']= pts_allowed
        total_games = (team_record['W'] + team_record['L'])[0]
        team_stats_df.drop(columns=['PLUS_MINUS'], inplace=True)
        team_stats_df = round((team_stats_df / total_games),1)




        return {
            "Team Name": self.team_name,
            "Team Record": team_record.to_dict(orient='records'),
            "Stats": team_stats_df.to_dict(orient='records'),
            "Advanced Stats": advanced_team_stats_df.to_dict(orient='records'),
             }



if __name__ == "__main__":
    team_analyzer = TeamAnalyzer("Golden State Warriors", "2025-26", "Regular Season")
    team_stats_test = team_analyzer.get_team_stats()
    print(team_stats_test)