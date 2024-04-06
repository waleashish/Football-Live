import streamlit as st
import json
from src.etl.bigquery.fixtures import get_all_fixtures

def handle_fixture_display():
    fixtures = get_all_fixtures()
    matchdays = fixtures["one_matchday"].unique()
    for x in matchdays:
        with st.expander(f"Matchday {x}"):
            matchday_df = fixtures.loc[fixtures["one_matchday"] == x, :]
            # We want to show the data as a fixture here, we have almost everything we need ... :)
            data = zip(
                matchday_df["one_crest"],
                matchday_df["one_home_team_name"],
                matchday_df["one_full_time_score"],
                matchday_df["one_half_time_score"],
                matchday_df["two_crest"],
                matchday_df["two_away_team_name"]
            )
            for (one_crest, one_name, ft_score, ht_score, two_crest, two_name) in data:
                row = st.columns(1)[0]
                home_info, score_info, away_info = row.columns(3)
                css_img = 'style="display:block; margin-left:auto; margin-right:auto; width:100px"'
                css_score = 'style="display:block; margin-left:auto; margin-right:auto; width:100px"'
                with home_info:
                    st.markdown(
                        f'<img src="{one_crest}" alt="Home Team Icon" {css_img}>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<span {css_img}>{one_name}</span>', 
                        unsafe_allow_html=True
                    )

                with score_info:
                    st.markdown(
                        f"<span {css_score}> {ft_score} </span>",
                        unsafe_allow_html=True
                    )

                with away_info:
                    st.markdown(
                        f'<img src="{two_crest}" alt="Away Team Icon" {css_img}>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<span {css_img}>{two_name}</span>', 
                        unsafe_allow_html=True
                    )