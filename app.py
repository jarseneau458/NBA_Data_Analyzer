import streamlit as st
import pandas as pd
from nba_api.stats.static.players import find_players_by_full_name
from nba_api.stats.static.teams import find_teams_by_full_name, get_teams
import altair as alt

from PlayerAnalyzer import PlayerAnalyzer
from TeamAnalyzerNew import TeamAnalyzer
from league_analyzer import get_league_leaders
from tab1 import render_trends_tabs
from tab2 import render_prop_line_analyzer
from tab3 import render_league_leaders_tab

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

    tab1, tab2, tab3 = st.tabs(["Season Trends", "Prop Analyzer", "League Leaders"])

    with tab1:
       render_trends_tabs(trends, analyzer, search_query, season, season_type)



    with tab2:
        render_prop_line_analyzer(analyzer)

    with tab3:
        render_league_leaders_tab(season, season_type)








