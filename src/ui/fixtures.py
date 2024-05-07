import streamlit as st
from src.load import get_data

def handle_fixture_display(competition):
    fixtures = get_data.get_fixtures(competition)
    matchdays = fixtures["matchday"].unique()

    print(f"Matchdays: {matchdays}")
    print(f"Data: {fixtures.head(5)}")
    for x in matchdays:
        with st.expander(f"Matchday {x}"):
            matchday_df = fixtures.loc[fixtures["matchday"] == x, :]
            # We want to show the data as a fixture here, we have almost everything we need ... :)
            data = zip(
                matchday_df["home_crest"],
                matchday_df["home_team"],
                matchday_df["home_score"],
                matchday_df["away_crest"],
                matchday_df["away_team"],
                matchday_df["away_score"],
                matchday_df["status"]
            )

            for (home_crest, home_team, home_score, away_crest, away_team, away_score, status) in data:
                row = st.columns(1)[0]
                home_info, score_info, away_info = row.columns(3)
                css_img = 'style="display:block; margin-left:auto; margin-right:auto; width:100px"'
                css_score = 'style="display:block; margin-left:auto; margin-right:auto; margin-top:50px; width:100px"'
                with home_info:
                    st.markdown(f"""
                    <div style="margin: 10px; text-align: center;">
                        <img src="{home_crest}" alt="Home Team Icon" {css_img}>
                        <h4 {css_img}>{home_team}</h4>
                    </div>
                    """, unsafe_allow_html=True)

                with score_info:
                    st.markdown(f"""
                    <div style="margin: 10px; text-align: center">
                        <h4 {css_score}> {home_score} - {away_score} </h4>
                    </div>
                    """, unsafe_allow_html=True)

                with away_info:
                    st.markdown(f"""
                                <div style="margin: 10px; text-align: center;">
                                    <img src="{away_crest}" alt="Away Team Icon" {css_img}>
                                    <h4 {css_img}>{away_team}</h4>
                                </div>
                                """, unsafe_allow_html=True)