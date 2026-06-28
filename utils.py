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