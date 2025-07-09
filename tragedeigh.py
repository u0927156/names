# %%
# Imports
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import numpy as np

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

# %%

year_cols = [col for col in male_df.columns if col.isnumeric()]
years = [int(year) for year in year_cols]
leigh_df = female_df[female_df.index.str.endswith("leigh")]

total_names_ending_in_leigh = leigh_df[year_cols].sum()
total_names = female_df[year_cols].sum()

fig = go.Figure()

fig.add_trace(go.Scatter(x=years, y=total_names_ending_in_leigh))

fig.update_layout(
    xaxis=dict(range=[1970, 2022], title="Year"),
    yaxis_title="Number of Girls",
    title="Number of Girls with Name ending in -leigh by year",
)

# %%

frames = []
keep_showing = []
years_to_show = [1930, 1950, 1970, 1990, 2010, 2023]
for y in [str(y) for y in years_to_show]:
    curr_series = female_df[y]

    filtered_series = curr_series[curr_series != 0]
