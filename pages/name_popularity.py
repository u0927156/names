import streamlit as st
import pandas as pd
from pathlib import Path
import jellyfish


from names.name_utils import convert_number_to_rate, add_sound_columns
from names.name_by_time import plot_name_popularity_by_time

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
