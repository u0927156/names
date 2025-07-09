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

proportions = []
years_to_show = list(range(1940, 2024))


fig = go.Figure()

for n in [10, 50, 100]:
    proportions = []
    for y in [str(y) for y in years_to_show]:
        curr_series = female_df[y]

        filtered_series = curr_series[curr_series != 0]
        num_people_with_top_n_names = (
            filtered_series.sort_values(ascending=False).iloc[:n].sum()
        )
        total_names = filtered_series.sum()

        proportion_with_top_n_names = (num_people_with_top_n_names / total_names) * 100
        proportions.append(proportion_with_top_n_names)
    fig.add_trace(go.Scatter(x=years_to_show, y=proportions, name=f"Top {n} Names"))

fig.update_layout(
    title=f"Percent of Girls with Top Names",
    xaxis_title="Year",
    yaxis_title="Percent",
)

# %%
# Find missing names
birth_df = pd.read_csv(
    "/home/spencer_dev/PythonProjects/names/birth_data/NCHS_-_Births_and_General_Fertility_Rates__United_States_20250709.csv"
)
birth_df["expected_number_of_boys"] = birth_df["Birth Number"] * 0.505
birth_df["expected_number_of_girls"] = birth_df["Birth Number"] * 0.495
birth_df = birth_df[birth_df["Year"] >= 1940]


total_recorded_births = female_df[birth_df["Year"].astype(str)].sum()

people_with_missing_names = birth_df["expected_number_of_girls"].reset_index(
    drop=True
) - total_recorded_births.reset_index(drop=True)

missing_fig = go.Figure()

missing_fig.add_trace(
    go.Scatter(
        x=birth_df["Year"],
        y=people_with_missing_names,
    )
)
missing_fig.update_layout(
    title=f"Estimated Number of Girls with Uncommon Names",
    xaxis_title="Year",
    yaxis_title="Number of Girls",
)
