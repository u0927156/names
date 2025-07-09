import streamlit as st
import pandas as pd
from pathlib import Path
import jellyfish


from names.name_utils import convert_number_to_rate
from names.name_by_time import plot_history_of_top_n_names_from_year

name_data_path = Path("./processed_data")

female_df = pd.read_csv(name_data_path / "female_names.csv", index_col=0)
male_df = pd.read_csv(name_data_path / "male_names.csv", index_col=0)

female_rate_df = convert_number_to_rate(female_df)
male_rate_df = convert_number_to_rate(male_df)

selected_year = st.slider("Select Year:", 1880, 2023, key="sdr_select_year", value=1984)


fig = plot_history_of_top_n_names_from_year(
    st.session_state.selected_df, 10, str(selected_year)
)
if st.session_state.use_rate:
    fig.update_layout(yaxis_title="Rate")
else:
    fig.update_layout(yaxis_title="Number of Children Named")

st.plotly_chart(fig)
