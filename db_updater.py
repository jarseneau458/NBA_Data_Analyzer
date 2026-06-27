import time
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players


load_dotenv()
db_password = os.getenv("DB_PASSWORD")
db_url = f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/nba_data"
engine = create_engine(db_url)

#Commonly searched players, added directly to database so no api call is needed
target_players= [
    "Nikola Jokic", "Luka Doncic", "Shai Gilgeous-Alexander", "Giannis Antetokounmpo", "Joel Embiid",
    "Anthony Edwards", "Jalen Brunson", "Stephen Curry", "Kevin Durant", "LeBron James", "Anthony Davis",
    "Devin Booker", "Tyrese Haliburton", "Donovan Mitchell", "De'Aaron Fox", "Domantas Sabonis",
    "Victor Wembanyama", "Zion Williamson", "Damian Lillard", "Kyrie Irving",

    # --- Tier 2: High-Usage All-Stars & Co-Stars ---
    "Tyrese Maxey", "Paul George", "Bam Adebayo", "Jimmy Butler", "Karl-Anthony Towns", "Jamal Murray",
    "Chet Holmgren", "Jalen Williams", "Paolo Banchero", "Franz Wagner", "Trae Young", "LaMelo Ball",
    "Ja Morant", "Jaren Jackson Jr.", "Desmond Bane", "DeMar DeRozan", "Pascal Siakam", "Myles Turner",
    "Julius Randle", "Rudy Gobert", "Mikal Bridges", "OG Anunoby",

    # --- Tier 3: Elite Role Players & Primary Initiators ---
    "Evan Mobley", "Darius Garland", "Jarrett Allen", "Bradley Beal", "CJ McCollum", "Brandon Ingram",
    "Alperen Sengun", "Fred VanVleet", "Jalen Green", "Scottie Barnes", "Immanuel Quickley", "RJ Barrett",
    "Cade Cunningham", "Jalen Duren", "Lauri Markkanen", "Tyler Herro", "D'Angelo Russell", "Austin Reaves",

    # --- Tier 4: Rebounders, Shooters, & Frequent Parlay Legs ---
    "Draymond Green", "Jonathan Kuminga", "Aaron Gordon", "Michael Porter Jr.", "Klay Thompson",
    "Kawhi Leonard", "James Harden", "Norman Powell", "Coby White", "Zach LaVine", "Nikola Vucevic",
    "Cam Thomas", "Nic Claxton", "Anfernee Simons", "Deandre Ayton", "Jerami Grant", "Kyle Kuzma",
    "Jordan Poole", "Miles Bridges"
]
#gets the players and their data
for index, player in enumerate(target_players):
    player_id = players.find_players_by_full_name(player)[0]['id']
    log = playergamelog.PlayerGameLog(player_id, season='2025-26')
    df = log.get_data_frames()[0]

    try:
        # if first player, use replace to wipe out old data, every player after, use append
        if index == 0:
            df.to_sql('player_game_log', engine, if_exists='replace')
        else:
            df.to_sql('player_game_log', engine, if_exists='append')

        time.sleep(4)

    except Exception as e:
        print(f"Error processing {player}: {e}")


print("Data is succesfully updated")
