import streamlit as st
import pandas as pd
from pyarrow.lib import nulls

from PlayerAnalyzer import PlayerAnalyzer, get_player_seasons

# Page Configuration
st.set_page_config(page_title="NBA Player Analyzer", layout="wide")


if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None



st.title("🏀 NBA Prop Analyzer", text_alignment="center")

# Center subheader
st.markdown("<h2 style='text-align: center;'>Welcome to the NBA Data Analyzer</h3>", unsafe_allow_html=True,)


st.markdown("<h3 style='text-align: center;'>Enter player name om the ""Player Search tab"" to get started</p>", unsafe_allow_html=True)

st.sidebar.header("Player Search")
player_name = st.sidebar.text_input("Enter player name:", value="")

avalible_seasons = []
if player_name.strip():
    with st.spinner("Loading player data..."):
        avalible_seasons = get_player_seasons(player_name)

if avalible_seasons:
    season = st.sidebar.text_input("Enter Season:", value="2025-26")
else:
    season =st.sidebar.text_input("Enter a Season:", value="2025-26")

season_type = st.sidebar.selectbox(
    "Select season type:",
    ("Regular Season", "Playoffs", "All Star Game")
)

button_text = "Analyze Player"

if st.sidebar.button(button_text):
    try:
        with st.spinner(f"Analyzing {player_name}..."):
            st.session_state.analyzer = PlayerAnalyzer(player_name, season, season_type)
        st.success(f"Loaded {player_name}'s data successfully!")
    except Exception as e:
        st.error(f"Error loading data: {e}")

if st.session_state.analyzer:
    analyzer = st.session_state.analyzer
    trends = analyzer.get_trends()
    current_tabs = st.radio("Navigation", ["Season Trends", "Prop Analyzer"],
                            horizontal=True,
                            label_visibility="collapsed")


    if current_tabs == "Season Trends":
        st.header(f"Performance for {player_name} in {season_type} {season}")
        st.subheader("General Trends")
        st.json(trends["Season Averages"])

        st.subheader("Last 5 Games Log")
        st.dataframe(trends["Last 5 Games"], use_container_width=True)

    elif current_tabs == "Prop Analyzer":
        st.header("Prop Line Analyzer")
        stat = st.selectbox("Choose Stat", analyzer.stats_tracked, index=15)
        line = st.number_input("Enter Prop Line", value=20.5, step=0.5, format="%.1f")
            #DEBUGGING: Print the return type to the UI so we can see what's wrong
        if st.button("Run Prop Analylisis"):
            result = analyzer.prop_line_analyzer(stat, line)

            if isinstance(result, dict):
                st.write(f"### {result.get('Name', 'Unknown')} ({result.get('Team', 'N/A')})")
                col1, col2 = st.columns(2)
                col1.metric("Season Over Rate", f"{result.get('Season Over Rate', 0)}%")
                col2.metric("Last 10 Over Rate", f"{result.get('Last 10 Over Rate', 0)}%")
                st.json(result)
            elif isinstance(result, str):
                st.warning(f"Prop Analyzer returned a message: {result}")
            else:
                st.error(f"Unexpected result format: {result}")













