import pandas as pd
import streamlit as st
from league_analyzer import get_league_leaders

def render_league_leaders_tab(season, season_type):
    st.header("League Leaders")
    min_games = st.number_input("Minimum Games Played", value=40, step=10)
    leaders = get_league_leaders(min_games, season, season_type)
    leaders_df = pd.DataFrame(leaders).T
    st.dataframe(leaders_df)