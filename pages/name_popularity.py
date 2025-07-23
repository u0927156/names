import streamlit as st
import pandas as pd
from pathlib import Path
import jellyfish


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

st.markdown(
    """
            # Name Popularity
            This page lets you view the popularity of a name and similar sounding names over time.

            You can toggle between showing the total number of people given a certain a year or the rate 
            of people given that year. 

            """
)


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

st.set_page_config(page_title="Search Popularity by Name")

selected_name = st.text_input("Search a Name:", value="Spencer")

show_similar_names = st.toggle("Show Similar Names", key="tgl_show_similar_names")
name_popularity_fig = plot_name_popularity_by_time(
    st.session_state.selected_df, selected_name, show_similar_names
)
if name_popularity_fig is not None:
    if st.session_state.use_rate:
        name_popularity_fig.update_layout(yaxis_title="Rate")
    else:
        name_popularity_fig.update_layout(yaxis_title="Number of Children Named")

    st.plotly_chart(name_popularity_fig)
else:
    st.write(
        f"Name: {selected_name} not found. Maybe this is an opportunity to be unique."
    )
