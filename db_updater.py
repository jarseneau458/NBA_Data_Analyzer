import time
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players


def update_player_database(max_players=None):
    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    db_url = f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/nba_data"
    engine = create_engine(db_url)

    active_roster = players.get_active_players()

    if max_players:
     active_roster = active_roster[:max_players]

    # Commonly searched players, added directly to database so no api call is needed

    # loops through each player to get game logs
    for index, player in enumerate(active_roster):
        player_name = player['full_name']
        player_id = player['id']

        print(f"Processing {player_name} ({player_id})")

        try:
            # get most recent season game logs
            log = playergamelog.PlayerGameLog(player_id, season='2025-26')
            df = log.get_data_frames()[0]

            if df.empty:
                print(f"No data found for {player_name}")
                continue

            # match db case
            df['Player_ID'] = player_id

            # if first player, use replace to wipe out old data, every player after, use append
            if index == 0:
                df.to_sql('player_game_log', engine, if_exists='replace')
            else:
                df.to_sql('player_game_log', engine, if_exists='append')

        except Exception as e:
            print(f"Error processing {player}: {e}")
        # rate limiting
        time.sleep(3.5)

    print("Data is succesfully updated")

if __name__ == "__main__":
    update_player_database(max_players=5)
