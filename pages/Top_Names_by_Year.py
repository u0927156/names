import streamlit as st
import pandas as pd
from pathlib import Path
import jellyfish


from names.name_utils import convert_number_to_rate, add_sound_columns
from names.name_by_time import plot_history_of_top_n_names_from_year


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
            # Top Names by Year

            This page lets you look at the top names by year. You can view this for males and females and by the total number
            of people given a name or the rate of people given that name. The sliders below control which year to look at 
            and how many of the top names, up to 25, you want to see.
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

selected_year = st.slider("Select Year:", 1880, 2024, key="sdr_select_year", value=1984)
num_names_to_look_at = st.slider(
    "Nmber of Names:", 1, 25, key="sdr_select_top_names", value=10
)


fig = plot_history_of_top_n_names_from_year(
    st.session_state.selected_df, num_names_to_look_at, str(selected_year)
)
fig.update_layout(showlegend=True)
if st.session_state.use_rate:
    fig.update_layout(yaxis_title="Rate")
else:
    fig.update_layout(yaxis_title="Number of Children Named")

st.plotly_chart(fig)
