
from nba_api.stats.static.teams import find_teams_by_full_name

#Stores methods used by both PlayerAnalyzer and TeamAnalyzer
class BaseAnalyzer:

    def get_matchup_trends(self, opponent):
        opponent = find_teams_by_full_name(opponent)[0]['abbreviation']
        matchup_df = self.df[self.df['MATCHUP'].str.contains(opponent, na=False)]
        if len(matchup_df) == 0:
            return {"No matchups found for the given opponent."}
        matchup_avgs = matchup_df[self.stats_tracked].mean().round(1).to_dict()

        return{"Opponent": opponent,"Games Played": len(matchup_df),
            "Matchup Averages": matchup_avgs,
            "Head-to-Head Record": matchup_df['WL'].value_counts().to_dict(),
            "Matchup Game Log": matchup_df.drop(columns=self.hidden_columns, errors='ignore')
               }


    def calculate_projections(self, stat_category, opponent):
        """ Calculates the projections of a player against another team."""
        if self.df.empty:
            return {"No data found for the given player."}
        if stat_category not in self.stats_tracked:
            return {f"{stat_category} is not a valid stat category."}
        season_avgs = self.df[stat_category].mean()

        l5_avgs = self.last_5[stat_category].mean()

        opponent_upper = opponent.upper()
        matchup_df = self.df[self.df['MATCHUP'].str.contains(opponent_upper, na = False)]

        if len(matchup_df) > 0:
            matchup_avgs = matchup_df[stat_category].mean()
            stat_projection = (season_avgs * .50) + (matchup_avgs * .20) + (l5_avgs * .30)
            used_matchup_data = True
        else:
            matchup_avgs = 0
            stat_projection = (season_avgs * .60) + (l5_avgs * .40)
            used_matchup_data = False
        return {
            "Opponent": opponent,
            "Projections": float(round(stat_projection,1)),
            "Season Averages": float(round(season_avgs, 1)),
            "Last 5 Averages": float(round(l5_avgs,1)),
            "Matchup Avg": float(round(matchup_avgs, 1)) if used_matchup_data else "N/A",
            "Matchup Games Played": len(matchup_df)
            }