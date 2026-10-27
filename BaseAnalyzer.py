from nba_api.stats.static.teams import find_teams_by_full_name

#Stores methods used by both PlayerAnalyzer and TeamAnalyzer
class BaseAnalyzer:
    def __init__(self):
        self.df = None
        self.last_10 = None
        self.last_5 = None
        self.stats_tracked = None
        self.hidden_columns = None
        self.full_name = None

    def get_matchup_trends(self, opponent):
        opponent = find_teams_by_full_name(opponent)[0]['abbreviation']
        matchup_df = self.df[self.df['MATCHUP'].str.contains(opponent, na=False)]
        if len(matchup_df) == 0:
            return {"No matchups found for the given opponent."}
        matchup_avgs = matchup_df[self.stats_tracked].mean().round(1).to_dict()

        return{"Opponent": opponent,"Games Played": len(matchup_df),
            "Matchup Averages": matchup_avgs,
            "Head-to-Head Record": matchup_df['WL'].value_counts().to_dict(),
            "Matchup Game Log": matchup_df[['GAME_DATE', 'MATCHUP', 'WL'] + self.stats_tracked]
               }

    def prop_line_analyzer(self, stat_category, prop_line):
        """Calculates the hit rate of a stat category based on the stat line."""

        if self.df.empty:
            return {"No data found for the given search."}
        if stat_category not in self.stats_tracked:
            return {f"{stat_category} is not a valid stat category."}

        team_abbr = self.df["MATCHUP"].iloc[0].split(" ")[0]

        # adds up the hit rates
        season_hits_over = int((self.df[stat_category] >= prop_line).sum())
        season_hits_under = int(len(self.df) - season_hits_over)
        l10_hits_over = (int((self.last_10[stat_category] >= prop_line).sum()))
        l10_hits_under = int(len(self.last_10) - l10_hits_over)
        l5_hits_over = int((self.last_5[stat_category] >= prop_line).sum())
        l5_hits_under = int(len(self.last_5) - l5_hits_over)

        total_games = len(self.df)
        l10_games = len(self.last_10)
        l5_games = len(self.last_5)

        # dosen't calculate up over/under rate if player has played 0 games
        if total_games != 0:
            season_over_rate = int(round((season_hits_over / len(self.df)) * 100, 2))
            season_under_rate = 100 - season_over_rate
        else:
            season_over_rate = 0
            season_under_rate = 0

        if l10_games != 0:
            l10_over_rate = int(round((l10_hits_over / 10) * 100, 2))
            l10_under_rate = 100 - l10_over_rate
        else:
            l10_over_rate = 0
            l10_under_rate = 0

        if l5_games != 0:
            l5_over_rate = int(round((l5_hits_over / 5) * 100, 2))
            l5_under_rate = 100 - l5_over_rate
        else:
            l5_over_rate = 0
            l5_under_rate = 0

        return {
            "Name": self.full_name,
            "Team": team_abbr,
            "Stats Category": stat_category.upper(),
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
            #simple formula used for the projection
            stat_projection = (season_avgs * .50) + (matchup_avgs * .20) + (l5_avgs * .30)
            used_matchup_data = True
        else:
            matchup_avgs = 0
            #fallback if no matchups have been played for that specific team
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