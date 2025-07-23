from functools import reduce


import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from names.name_utils import convert_number_to_rate


def get_name_df(name, selected_df):
    name_df = pd.DataFrame(selected_df.loc[name].iloc[-99:]).reset_index(names="year")
    name_df[f"{name}_prob"] = name_df[name] / name_df[name].sum()

    name_df["year"] = name_df["year"].astype("Int64")

    return name_df


def estimate_age(
    names_genders: list[tuple], male_df, female_df, birth_year_population_df
):

    all_name_dfs = []
    for name, gender in names_genders:
        if gender == "male":
            selected_df = male_df
        else:
            selected_df = female_df

        if name not in selected_df.index:
            raise ValueError(f"{name} was not found in the records for {gender}s.")

        curr_name_df = get_name_df(name, selected_df)

        all_name_dfs.append(curr_name_df)

    name_df = reduce(
        lambda left, right: pd.merge(left, right, on="year", how="inner"), all_name_dfs
    )

    population_pyramid_to_add = f"{names_genders[0][1]}_prob"
    combined_df = birth_year_population_df.merge(name_df, on="year", how="inner")

    combined_df["combined_probability"] = combined_df[
        [f"{name}_prob" for name, _ in names_genders] + [population_pyramid_to_add]
    ].prod(axis=1)

    combined_df["combined_probability"] = (
        combined_df["combined_probability"] / combined_df["combined_probability"].sum()
    )
    most_common_idx = combined_df["combined_probability"].idxmax()
    most_common_year = combined_df.loc[most_common_idx]["year"]

    expected_value = (combined_df["year"] * combined_df["combined_probability"]).sum()

    std_year = np.sqrt(
        (
            np.pow((combined_df["year"] - expected_value), 2)
            * combined_df["combined_probability"]
        ).sum()
    )

    return most_common_year, expected_value, std_year, combined_df
