from league_analyzer import get_league_leaders
from db_updater import update_player_database, update_custom_list, update_single_player
from PlayerAnalyzer import PlayerAnalyzer


def main_menu():
    """
    Displays the main menu for the NBA Data Analyzer application and handles user
    interactions for various functionalities.
    """
    while True:
        print("\n--- NBA Data Analyzer ---")
        print("1. Analyze Player Prop Line")
        print("2. Get Player Trends & Matchups")
        print("3. Get League Leaders")
        print("4. Update Database (League/Batch)")
        print("5. Update Database (Single Player)")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter player name: ")
            season, season_type = get_season_info()
            stat_category = input("Enter the stat category (e.g., PTS, REB, AST): ")



            try:
                prop_line = float(input("Enter the prop line (ex. 20.5): "))
            except ValueError:
                print("Invalid prop line. Please enter a number.")
                continue

            print(f"Analyzing {name} ({stat_category} - {prop_line})...")
            analyzer = PlayerAnalyzer(name, season=season, season_type=season_type)
            print("\n", analyzer.prop_line_analyzer(stat_category, prop_line))

        elif choice == "2":
            name = input("Enter player name: ")
            season, season_type = get_season_info()
            opp = input("Enter opponent abbreviation (ex. TOR): ")

            print(f"Getting {name} trends and matchups...")
            analyzer = PlayerAnalyzer(name, season=season, season_type=season_type)

            print(f"Trends against {opp}:")
            print(analyzer.get_matchup_trends(opp))

        elif choice == "3":
            print("Calculating league leaders...")
            season, season_type = get_season_info()

            try:
                min_games = int(input("Enter the minimum number of games played: "))

            except ValueError:
                min_games = 40

            leaders = get_league_leaders(min_games, season=season, season_type=season_type)

            print("\n--- LEAGUE LEADERS SUMMARY ---")
            for stat, data in leaders.items():
                print(f"{stat} Leader: {data['Player']} ({data['Average']} per game)")

        elif choice == "4":
            user_input = input(" Enter list of players to update (comma-separated): ")
            season, season_type = get_season_info()
            player_list = []

            for name in user_input.split(","):
                name_stripped = name.strip()
                if name_stripped:
                    player_list.append(name_stripped)

            if player_list:
                update_custom_list(player_list, season, season_type)
                print(f"Successfully processed {len(player_list)} players in the database.")
            else:
                print("No players entered.")





        elif choice == "5":
            name = input("Enter Player Name: ")
            season, season_type = get_season_info()

            print(f"Updating {name}...")
            update_player_database(
                name,
                season=season,
                season_type=season_type
            )

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


def get_season_info():
    """
    Collects season information including season year and type from user input.
    """
    season = input("Enter the season (e.g., 2025-26): ")

    if not season:
        season = "2025-26"

    season_type = input(
        "Enter the season type by entering 1, 2, or 3 "
        "(1. Regular Season, 2. Playoffs, 3. All Star): "
    )

    if season_type == "1":
        season_type = "Regular Season"
    elif season_type == "2":
        season_type = "Playoffs"
    elif season_type == "3":
        season_type = "All Star Game"
    else:
        season_type = "Regular Season"

    return season, season_type


if __name__ == "__main__":
    main_menu()