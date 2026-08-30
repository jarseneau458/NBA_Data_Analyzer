import pandas as pd
import streamlit as st
from PlayerAnalyzer import PlayerAnalyzer
from TeamAnalyzerNew import TeamAnalyzer


def render_trends_tabs(trends, analyzer, search_query, season, season_type):
    if isinstance(analyzer, PlayerAnalyzer):
        st.header(f"Performance for {search_query} in {season_type} {season}")
        st.subheader("General Trends")
        season_avg_df = pd.DataFrame([trends["Season Averages"]])
        st.dataframe(season_avg_df, use_container_width=True, hide_index=True)

        st.subheader("Last 5 Games Log")
        st.dataframe(trends["Last 5 Games"], use_container_width=True, hide_index=True)
    elif isinstance(analyzer, TeamAnalyzer):
        st.header(f"Performance for {search_query} in {season_type} {season}")
        st.subheader("Team Stats")
        team_stats_df = pd.DataFrame(trends["Stats"])
        st.dataframe(team_stats_df, use_container_width=True, hide_index=True)

        st.subheader("Advanced Team Stats")
        advanced_stats_df = pd.DataFrame(trends["Advanced Stats"])
        st.dataframe(advanced_stats_df, use_container_width=True, hide_index=True)
