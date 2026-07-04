import streamlit as st
import pandas as pd
from pyarrow.lib import nulls

from PlayerAnalyzer import PlayerAnalyzer


# Page Configuration
st.set_page_config(page_title="NBA Player Analyzer", layout="wide")


if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None



st.title("🏀 NBA Prop Analyzer", text_alignment="center")

# Center a subheader
st.markdown("<h2 style='text-align: center;'>Welcome to the NBA Data Analyzer</h3>", unsafe_allow_html=True,)

# Center regular body text
st.markdown("<h3 style='text-align: center;'>Enter player name to get started</p>", unsafe_allow_html=True)

st.sidebar.header("Player Search")





