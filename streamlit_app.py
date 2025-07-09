import streamlit as st
import pandas as pd
from pathlib import Path


from names.name_utils import convert_number_to_rate, add_sound_columns
from names.name_by_time import plot_name_popularity_by_time


name_data_path = Path("./processed_data")

female_df = pd.read_csv(name_data_path / "female_names.csv", index_col=0)
male_df = pd.read_csv(name_data_path / "male_names.csv", index_col=0)

female_rate_df = convert_number_to_rate(female_df)
male_rate_df = convert_number_to_rate(male_df)

male_df = add_sound_columns(male_df)
female_df = add_sound_columns(female_df)
female_rate_df = add_sound_columns(female_rate_df)
male_rate_df = add_sound_columns(male_rate_df)


st.write("# Name App++")

selected_gender = st.radio(label="Sex", options=["Male", "Female"])
use_rate = st.toggle("Use Relative Rate of Names", key="tgl_use_rate")

if selected_gender == "Male":
    if use_rate:
        selected_df = male_rate_df
    else:
        selected_df = male_df
else:
    if use_rate:
        selected_df = female_rate_df
    else:
        selected_df = female_df

st.session_state.use_rate = use_rate
st.session_state.selected_df = selected_df

pg = st.navigation(
    [st.Page("pages/name_popularity.py"), st.Page("pages/Top_Names_by_Year.py")]
)
pg.run()
