import streamlit as st
import pandas as pd
from nba_api.stats.static.players import find_players_by_full_name
from nba_api.stats.static.teams import find_teams_by_full_name, get_teams
import altair as alt

from PlayerAnalyzer import PlayerAnalyzer
from TeamAnalyzerNew import TeamAnalyzer

st.set_page_config(page_title="NBA Player Analyzer", layout="wide")

if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None

st.title("NBA Player Analyzer", text_alignment="center")
st.markdown("<h2 style='text-align: center;'>Welcome to the NBA Data Analyzer</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Enter player or team name on the search tab to get started</h3>", unsafe_allow_html=True)

st.sidebar.header("Search")
search_query = st.sidebar.text_input("Enter player or team name:", value="", key="search_query")
season = st.sidebar.text_input("Enter season (e.g., 2025-26):", value="2025-26")
season_type = st.sidebar.selectbox("Select season type:", ("Regular Season", "Playoffs", "All Star Game"))

if st.sidebar.button("Analyze"):

    #clears the previous state data when new player or team is searched
    if 'analyze_stat' in st.session_state:
        del st.session_state['analyze_stat']

    if 'analyze_team' in st.session_state:
        del st.session_state['analyze_team']
    try:
        with st.spinner(f"Analyzing {search_query}..."):
            team_search = find_teams_by_full_name(search_query)
            player_search = find_players_by_full_name(search_query)

            if team_search:
                st.session_state.analyzer = TeamAnalyzer(search_query, season, season_type)
                st.success(f"Loaded {search_query}'s data successfully!")
            elif player_search:
                st.session_state.analyzer = PlayerAnalyzer(search_query, season, season_type)
                st.success(f"Loaded {search_query}'s data successfully!")
            else:
                st.error(f"No player or team found with the name: {search_query}")
    except Exception as e:
        st.error(f"Error loading data: {e}")

if st.session_state.analyzer:
    analyzer = st.session_state.analyzer
    if isinstance(analyzer, PlayerAnalyzer):
        trends = analyzer.get_trends()
    else:
        trends = analyzer.get_team_stats()

    current_tabs = st.radio("Navigation", ["Season Trends", "Prop Analyzer"], horizontal=True, label_visibility="collapsed")

    if current_tabs == "Season Trends":
        if isinstance(analyzer, PlayerAnalyzer):
            st.header(f"Performance for {search_query} in {season_type} {season}")
            st.subheader("General Trends")
            season_avg_df = pd.DataFrame([trends["Season Averages"]])
            st.dataframe(season_avg_df, use_container_width=True, hide_index=True)

            st.subheader("Last 5 Games Log")
            st.dataframe(trends["Last 5 Games"], use_container_width=True, hide_index=True)
        else:
            st.header(f"Performance for {search_query} in {season_type} {season}")
            st.subheader("Team Stats")
            team_stats_df = pd.DataFrame(trends["Stats"])
            st.dataframe(team_stats_df, use_container_width=True, hide_index=True)

            st.subheader("Advanced Team Stats")
            advanced_stats_df = pd.DataFrame(trends["Advanced Stats"])
            st.dataframe(advanced_stats_df, use_container_width=True, hide_index=True)


    elif current_tabs == "Prop Analyzer":

        st.header("Prop Line Analyzer")

        stat = st.selectbox("Choose Stat", analyzer.stats_tracked, index=0)
        line = st.number_input("Enter Prop Line", value=20.5, step=0.5, format="%.1f")
        team_names = [team['full_name'] for team in get_teams()]
        # default if user doesn't pick a specific team
        team_names.insert(0, "None")


        if st.button("Run Prop Analysis"):
            st.session_state.analyze_stat = pd.DataFrame([analyzer.prop_line_analyzer(stat, line)])




        if 'analyze_stat' in st.session_state:

            result = st.session_state.analyze_stat

            col1, col2 = st.columns(2)
            col1.metric("Season Over Rate", f"{result['Season Over Rate'].iloc[0]}%")
            col2.metric("Last 10 Over Rate", f"{result['Last 10 Over Rate'].iloc[0]}%")

            chart_df = analyzer.df[['GAME_DATE', 'MATCHUP', stat]].copy()
            chart_df['GAME_DATE'] = pd.to_datetime(chart_df['GAME_DATE'])
            chart_df = chart_df.sort_values('GAME_DATE').tail(10)

            bars = alt.Chart(chart_df).mark_bar().encode(
                x=alt.X('MATCHUP', title='Opponent', sort=alt.EncodingSortField(field='GAME_DATE', order='ascending')),
                y=alt.Y(stat, title=stat),
                tooltip=['GAME_DATE', 'MATCHUP', stat]
            )

            threshold = alt.Chart(pd.DataFrame({'threshold': [line]})).mark_rule(color='red', size=2,
                                                                                 opacity=0.8).encode(
                y=alt.Y('threshold', title='Prop Line')

            )

            st.altair_chart(bars + threshold, use_container_width=True)
            st.dataframe(result.T.drop(['Name', 'Team']).rename(columns={0: ''}))


        team_selection = st.selectbox("Select Team", team_names, index=0)
        if st.button("Analyze Matchups for Team"):

            if team_selection != "None":
                st.session_state.analyze_team = analyzer.get_matchup_trends(team_selection)

        if 'analyze_team' in st.session_state:
            results = st.session_state.analyze_team
            st.dataframe(results['Matchup Averages'])
            st.dataframe(results['Matchup Game Log'])







