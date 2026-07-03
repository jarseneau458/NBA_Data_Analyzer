import time
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players


def update_player_database(max_players=None, season='2025-26', season_type='Regular Season'):
    """
    Updates the player database with game log data for active players in the NBA. The function retrieves the
    active player list, optionally limits the number of players processed, fetches their game log data for
    the specified season, and stores it in a database. It uses the NBA API and stores the logs in a
    PostgreSQL database.

    """
    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    db_url = f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/nba_data"
    engine = create_engine(db_url)

    active_roster = players.get_active_players()

    if max_players:
        active_roster = active_roster[:max_players]
        first_player = active_roster[0]
        first_log = playergamelog.PlayerGameLog(first_player['id'], season=season, season_type_all_star=season_type)

        df = first_log.get_data_frames()[0]
        df['Player_ID'] = first_player['id']
        df.to_sql('player_game_log', engine, if_exists='replace', index=False)

        time.sleep(3.5)

    for player in active_roster[1:]:
        player_name = player["full_name"]
        player_id = player["id"]

        print(f"Processing {player_name}...")

        try:
            log = playergamelog.PlayerGameLog(
                player_id,
                season=season,
                season_type_all_star=season_type
            )
            df = log.get_data_frames()[0]

            if df.empty:
                continue

            df["Player_ID"] = player_id
            df.to_sql("player_game_log", engine, if_exists="append", index=False)

        except Exception as e:
            print(f"Error processing {player_name}: {e}")

        time.sleep(3.5)

    print("Data is successfully updated")

def update_single_player(player_name,season='2025-26', season_type='Regular Season'):
    """
    Updates the game log data for a single player in the database.

    This function retrieves a player's game log for a specific NBA season and updates the corresponding
    records in the database. It connects to the database using credentials from environment variables,
    queries the player's information based on their full name, and retrieves their game log data for
    the 2025-26 NBA season. If no data is available for the player, the function logs this condition
    and takes no further action. Otherwise, it writes the data to the database.
    """
    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    db_url = f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/nba_data"
    engine = create_engine(db_url)

    found_player = players.find_players_by_full_name(player_name)
    if not found_player:
        print(f"Player not found: {player_name}")
        return

    player_info = found_player[0]
    player_id = player_info['id']
    full_name = player_info['full_name']
    print(f"Processing {full_name}...")

    try:
        log = playergamelog.PlayerGameLog(player_id, season=season, season_type_all_star=season_type)
        df = log.get_data_frames()[0]
        if df.empty:
            print(f"No data found for {full_name}.")
            return
        df['Player_ID'] = player_id
        df.to_sql('player_game_log', engine, if_exists='replace', index = False)
        print(f"{full_name} is successfully updated.")
    except Exception as e:
        print(f"Error processing {full_name}: {e}")


if __name__ == "__main__":
    update_player_database(max_players=5)