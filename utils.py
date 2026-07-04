from nba_api.stats.static import teams
from nba_api.stats.static import players

def get_active_teams():
    return teams.get_teams()

def get_team_name_by_id(team_id):
    return teams.get_team_id_from_name(team_id)

def get_active_players():
    return players.get_active_players()

def get_player_name_by_id(player_id):
    try:
        clean_id = int(player_id)
        player_info = players.find_player_by_id(clean_id)
        if player_info:
            return player_info['full_name']
        else:
            return f"Player with ID {player_id} not found"
    except Exception as e:
        return f" Error with ID {player_id}: {e}"

def get_season_id(season, season_type):
    season_prefix = {
        "Regular Season": "2",
        "All Star": "3",
        "Playoffs": "4"
    }


    prefix = season_prefix.get(season_type)
    if prefix is None:
        raise ValueError("Invalid season type. Please use 'Regular Season', 'All Star Game', or 'Playoffs'.")
    return (
        #gets only the starting year numbers because nba database only stores the prefix plus the starting year nums
        prefix + season[:4]
    )


def get_season_info():
    """
    Collects season information including season year and type from user input.
    """
    season = input("Enter the season (e.g., 2025-26): ").strip()
    if not season:
        season = '2025-26'

    season_type_input = input("Enter season type (1. Regular Season, 2. Playoffs, 3. All Star): ").strip()
    if season_type_input == '2':
        season_type = 'Playoffs'
    elif season_type_input == '3':
        season_type = 'All Star Game'
    else:
        season_type = 'Regular Season'

    return season, season_type