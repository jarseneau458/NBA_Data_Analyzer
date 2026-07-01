from league_analyzer import get_league_leaders
from db_updater import update_player_database
from PlayerAnalyzer import PlayerAnalyzer


def main_menu():
    """
    Displays the main menu for the NBA Data Analyzer application and handles user
    interactions for various functionalities such as viewing league leaders, analyzing
    player prop lines, updating the player database, and exiting the program.

    The menu allows users to navigate through the following options:
    1. View League Leaders: Displays top performers in various statistical categories.
       Requires a minimum threshold of games played.
    2. Analyze Player Prop Line: Accepts player information and a statistical category,
       then computes and displays the probabilities of exceeding a given line for that category.
    3. Update Database: Allows updating the player database by specifying the number of players to update.
    4. Exit: Exits the testing program.

    The functionality is driven by user input, and each choice corresponds to specific actions
    or analysis based on the respective selection.
    """
    while True:
        print("n\====NBA Data Analyzer====\n")
        print("1. View League Leaders")
        print("2. Analyze player prop line")
        print("3.Update Database")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("You selected: Viewing League Leaders (min 30 games)")

            leaders = get_league_leaders(min_games=30)
            for stat, data in leaders.items():
                print(f"{stat} Leader: {data['Player']} ({data['Average']} per game)")


        elif choice == '2':
            print("You selected: Analyzing player prop line")
            player_name = input("Enter the player's name: ")
            stat_category = input("Enter the stat category (e.g., PTS, REB, AST): ").upper()
            prop_line = input("Enter the prop line (e.g., 25.5): ")

            print(f"Prop line analysis for {player_name} in {stat_category}: {prop_line}")


            print(f"Looking for {player_name} ")

            try:
                analyzer = PlayerAnalyzer(player_name)
                results = analyzer.prop_line_analyzer(stat_category=stat_category, prop_line=prop_line)

                print(f"--- {player_name.upper()} {stat_category} OVER {prop_line} ---")
                print(
                    f"Season Hit Rate:  {results['Season Over Rate']}% ({results['Season Over Hits']} / {results['Season Over Hits'] + results['Season Under Hits']} games)")
                print(f"Last 10 Hit Rate: {results['Last 10 Over Rate']}% ({results['Last 10 Over Hits']} / 10 games)")
                print(f"Last 5 Hit Rate:  {results['Last 5 Over Rate']}% ({results['Last 5 Over Hits']} / 5 games)")
                print("----------------------------------------\n")
            except Exception as e:
                print(f"Error: {e}")
                print("Check the spelling and try again.")


        elif choice == '3':
            print("You selected: Updating Database")
            num_players = input("How many players would you like to update?")
            try:
                num_players = int(num_players)
                update_player_database(num_players)
                print("Database updated successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue


        elif choice == '4':
            print("You selected: Exiting the program")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()


