import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from utils import get_player_name_by_id

def get_league_leaders(min_games=40):
    """
    Calculate league leaders based on various statistics for players meeting a minimum
    number of games played. The function connects to a database, retrieves player game
    log data, filters players based on the minimum games requirement, calculates
    averages for specified statistics, and identifies the players with the highest
    average in each statistic.
    """
    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    db_url = f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/nba_data"
    engine = create_engine(db_url)

    df = pd.read_sql('SELECT * FROM player_game_log', engine)
    if df.empty:
        print("No data found in the database.")
        return {}

    #filter players who meet the min games req
    game_counts = df.groupby('Player_ID').size()
    qualified_player_ids = game_counts[game_counts >= min_games].index
    filtered_df = df[df['Player_ID'].isin(qualified_player_ids)]

    stats_to_track = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG3M', 'FG3A', 'FTM', 'FTA', 'FGA', 'FGM' ]
    player_averages = filtered_df.groupby('Player_ID')[stats_to_track].mean()

    leaderboard = {}

    #loops through each stat to find the player id with highest avg ands adds that player to the leaderboard dict
    for stat in stats_to_track:
        top_players = player_averages[stat].idxmax()
        highest_averages = round(player_averages[stat].max(), 1)

        #converts player id to thier name to add to dict
        player_name = get_player_name_by_id(top_players)

        leaderboard[stat] = {
           "Player": player_name,
            "Average": highest_averages
        }

    return leaderboard


if __name__ == "__main__":

    leaders = get_league_leaders(min_games=10)

    print("\n--- LEAGUE LEADERS SUMMARY ---")
    for stat, data in leaders.items():
        print(f"{stat} Leader: {data['Player']} ({data['Average']} per game)")
