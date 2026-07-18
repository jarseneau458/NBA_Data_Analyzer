import pandas as pd
from nba_api.stats.endpoints import leagueleaders


def get_league_leaders(min_games=40, season='2025-26', season_type='Regular Season'):
    """
    Fetches the pre-calculated league leaders directly from the NBA API.
    Filters the results by a minimum games played threshold.
    """

    # Get the data directly from the NBA API's LeagueLeaders endpoint
    try:
        leaders = leagueleaders.LeagueLeaders(
            season=season,
            season_type_all_star=season_type,
            stat_category_abbreviation='PTS'  # We just use PTS to pull the master table
        )
        df = leaders.get_data_frames()[0]
    except Exception as e:
        print(f"Error fetching data from NBA API: {e}")
        return {}

    if df.empty:
        print("No data found.")
        return {}

    # 2. Filter players who meet the minimum games requirement
    filtered_df = df[df['GP'] >= min_games]

    if filtered_df.empty:
        print(f"No players found with at least {min_games} games played.")
        return {}

    stats_to_track = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG3M', 'FG3A', 'FTM', 'FTA', 'FGA', 'FGM']

    leaderboard = {}

    #  Loop through each stat to find the actual leader
    for stat in stats_to_track:

        #  divide the stat total by Games Played to get average .
        per_game_col = f"{stat}_PER_GAME"
        filtered_df[per_game_col] = filtered_df[stat] / filtered_df['GP']

        # Find the index of the row with the maximum per-game average
        leader_idx = filtered_df[per_game_col].idxmax()

        # Extract the player's name and average
        player_name = filtered_df.loc[leader_idx, 'PLAYER']
        highest_average = round(filtered_df.loc[leader_idx, per_game_col], 1)

        leaderboard[stat] = {
            "Player": player_name,
            "Average": highest_average
        }

    return leaderboard


if __name__ == "__main__":
    leaders = get_league_leaders(min_games=10)

    print("\n--- LEAGUE LEADERS SUMMARY ---")
    for stat, data in leaders.items():
        print(f"{stat} Leader: {data['Player']} ({data['Average']} per game)")