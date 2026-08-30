import streamlit as st
import pandas as pd
import altair as alt
from nba_api.stats.static.teams import get_teams


def render_prop_line_analyzer(analyzer):
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