# %%
# Imports
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import numpy as np

from names.name_utils import convert_number_to_rate, add_sound_columns
from names.name_by_time import plot_name_popularity_by_time


name_data_path = Path("./processed_data")
output_path = Path(".") / "output" / "tragedeigh_figures"

female_df = pd.read_csv(name_data_path / "female_names.csv", index_col=0)
male_df = pd.read_csv(name_data_path / "male_names.csv", index_col=0)

female_rate_df = convert_number_to_rate(female_df)
male_rate_df = convert_number_to_rate(male_df)

male_df = add_sound_columns(male_df)
female_df = add_sound_columns(female_df)
female_rate_df = add_sound_columns(female_rate_df)
male_rate_df = add_sound_columns(male_rate_df)

image_height = 600
image_width = 800
# %%

year_cols = [col for col in male_df.columns if col.isnumeric()]
range_cols = [y for y in year_cols if int(y) >= 1970]


def get_fig_of_names_ending_with(df, ending_with, girl_boy):

    year_cols = [col for col in df.columns if col.isnumeric()]
    years = [int(year) for year in year_cols]
    leigh_df = df[df.index.str.endswith(ending_with)]

    total_names_ending_in_leigh = leigh_df[year_cols].sum()

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=years, y=total_names_ending_in_leigh))

    fig.update_layout(
        xaxis=dict(range=[1970, 2024], title="Year"),
        yaxis_title=f"Number of {girl_boy}s",
        title=f"Number of {girl_boy}s with Name ending in -{ending_with} by year",
    )

    return fig, leigh_df


fig, leigh_df = get_fig_of_names_ending_with(female_df, "eigh", "Girl")


fig.add_vline(
    2021, annotation_text="r/tragedeigh founded", annotation_position="bottom left"
)
fig.show()
fig.write_image(output_path / "eigh.png", height=image_height, width=image_width)
fig.write_image(output_path / "eigh_cover.png", height=1080, width=1920)


# %%

fig, ynn_df = get_fig_of_names_ending_with(male_df, "ynn", "Boy")
fig.write_image(output_path / "ynn.png", height=image_height, width=image_width)
fig.show()
# fig, ynn_df = get_fig_of_names_ending_with(female_df, "ynn", "Boy")
# fig.write_image(output_path / "ynn.png", height=image_height, width=image_width)
# fig.show()

# %%

proportions = []
years_to_show = list(range(1940, 2025))


def get_top_n_names(df, years_to_show: list[int]):
    fig = go.Figure()

    for n in [10, 50, 100]:
        proportions = []
        for y in [str(y) for y in years_to_show]:
            curr_series = df[y]

            filtered_series = curr_series[curr_series != 0]
            num_people_with_top_n_names = (
                filtered_series.sort_values(ascending=False).iloc[:n].sum()
            )
            total_names = filtered_series.sum()

            proportion_with_top_n_names = (
                num_people_with_top_n_names / total_names
            ) * 100
            proportions.append(proportion_with_top_n_names)
        fig.add_trace(go.Scatter(x=years_to_show, y=proportions, name=f"Top {n} Names"))

    return fig


fig = get_top_n_names(female_df, years_to_show)
fig.update_layout(
    title=f"Percent of Girls with Top Names",
    xaxis_title="Year",
    yaxis_title="Percent",
    yaxis_range=[0, 100],
)
fig.show()
fig.write_image(
    output_path / "female_top_names.png", height=image_height, width=image_width
)

fig = get_top_n_names(male_df, years_to_show)
fig.update_layout(
    title=f"Percent of Boys with Top Names",
    xaxis_title="Year",
    yaxis_title="Percent",
    yaxis_range=[0, 100],
)
fig.show()
fig.write_image(
    output_path / "male_top_names.png", height=image_height, width=image_width
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
    xaxis_range=[1970, 2024],
)

# %%
# Specific Names


fig = go.Figure()

for name in [
    # "Ashleigh",
    # "Kayleigh",
    # "Ryleigh",
    # "Charleigh",
    "Mary",
    "Elizabeth",
    "Rachel",
    # "Jennifer",
]:
    year_cols = [col for col in female_df.columns if col.isnumeric()]
    years = [int(year) for year in year_cols]
    fig.add_trace(
        go.Scatter(
            x=years,
            y=female_df.loc[name][year_cols] / female_df.loc[name][year_cols].max(),
            name=name,
            line=dict(width=3),
        )
    )

    # fig = plot_name_popularity_by_time(female_df, n)
fig.update_layout(
    yaxis_title="Relative Popularity",
    xaxis_title="Year",
    xaxis_range=["1900", "2024"],
    title="Popularity Relative to Peak by Year of Baby Girl Names",
)
fig.write_image(
    output_path / "relative_popularity_girls.png",
    height=image_height,
    width=image_width,
)

# %%
# Boy
