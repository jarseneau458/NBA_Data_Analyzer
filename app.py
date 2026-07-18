import streamlit as st
import pandas as pd
from pyarrow.lib import nulls
import altair as alt

from PlayerAnalyzer import PlayerAnalyzer, get_player_seasons

# Page Configuration
st.set_page_config(page_title="NBA Player Analyzer", layout="wide")


if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None



st.title("NBA Player Analyzer", text_alignment="center")

# Center subheader
st.markdown("<h2 style='text-align: center;'>Welcome to the NBA Data Analyzer</h3>", unsafe_allow_html=True,)


st.markdown("<h3 style='text-align: center;'>Enter player name on the ""Player Search tab"" to get started</p>", unsafe_allow_html=True)

st.sidebar.header("Player Search")
player_name = st.sidebar.text_input("Enter player name:", value="", key="player_name")

avalible_seasons = []
if player_name.strip():
    with st.spinner("Loading player data..."):
        avalible_seasons = get_player_seasons(player_name)

if avalible_seasons:
    season = st.sidebar.selectbox("Enter Season:", avalible_seasons, index= 0)
else:
    season =st.sidebar.selectbox("Enter a Season:", avalible_seasons,  index=0)

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
        season_avg_df = pd.DataFrame([trends["Season Averages"]])
        st.dataframe(season_avg_df, use_container_width=True, hide_index=True)

        st.subheader("Last 5 Games Log")
        st.dataframe(trends["Last 5 Games"], use_container_width=True,hide_index=True)

    elif current_tabs == "Prop Analyzer":
        st.header("Prop Line Analyzer")
        stat = st.selectbox("Choose Stat", analyzer.stats_tracked, index=0)
        line = st.number_input("Enter Prop Line", value=20.5, step=0.5, format="%.1f")

        if st.button("Run Prop Analylisis"):
            st.session_state.analyze_stat =  result = pd.DataFrame([analyzer.prop_line_analyzer(stat, line)])


        if 'analyze_stat' in st.session_state:
            result = st.session_state.analyze_stat
            st.write(f"### {result['Name'].iloc[0]} ({result['Team'].iloc[0]})")
            col1, col2 = st.columns(2)
            col1.metric("Season Over Rate", f"{result['Season Over Rate'].iloc[0]}%")
            col2.metric("Last 10 Over Rate", f"{result['Last 10 Over Rate'].iloc[0]}%")

            chart_df = analyzer.df[['GAME_DATE', 'MATCHUP', stat]].copy()
            chart_df['GAME_DATE'] = pd.to_datetime(chart_df['GAME_DATE'])

            chart_df = chart_df.sort_values('GAME_DATE').tail(10)


            bars = alt.Chart(chart_df).mark_bar().encode(
                    x=alt.X('MATCHUP', title='Opponent', sort=alt.EncodingSortField(field='GAME_DATE', order='ascending')),
                    y=alt.Y(stat, title=stat),
                    tooltip=['GAME_DATE','MATCHUP' ,stat]
                )

            threshold= (alt.Chart(pd.DataFrame({'threshold': [line]})).mark_rule(color='red', size =2, opacity = 0.8)
                .encode(
                    y=alt.Y('threshold', title='Prop Line')
                ))
            st.altair_chart(bars + threshold, use_container_width=True)




            st.dataframe(result.T.drop(['Name', 'Team']).rename(columns={0: ''}))














