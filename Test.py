from PlayerAnalyzer import PlayerAnalyzer


analyzer = PlayerAnalyzer("Jaylen Brown")

opponent_input = input("\nEnter the 3-letter opponent abbreviation (e.g., NYK, LAL): ")
matchup_data = analyzer.get_matchup_trends(opponent_input)

print(f"\n--- CAREER VS {opponent_input.upper()} ---")
if "Error" in matchup_data:
    print(matchup_data["Error"])
else:
    print(f"Games Played: {matchup_data['Games Played']}")
    print(matchup_data["Matchup Averages"])




