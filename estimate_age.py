# %%
from functools import reduce


import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from names.name_utils import convert_number_to_rate

# %%
name_data_path = Path("./processed_data")

female_df = pd.read_csv(name_data_path / "female_names.csv", index_col=0)
male_df = pd.read_csv(name_data_path / "male_names.csv", index_col=0)

female_rate_df = convert_number_to_rate(female_df)
male_rate_df = convert_number_to_rate(male_df)

# %%

population_pyramid_df = pd.read_csv(
    "birth_data/United_States_(2025)_07-22-2025_1058_AM.csv"
)
population_pyramid_df.columns = ["Age", "Male", "Female"]

population_pyramid_df = population_pyramid_df.iloc[:20]

population_pyramid_df["Bracket Start Age"] = (
    population_pyramid_df["Age"].str.split("-").str[0]
)
population_pyramid_df["Bracket End Age"] = (
    population_pyramid_df["Age"].str.split("-").str[1]
)

birth_years = []
male_population = []
female_population = []
for i, row in population_pyramid_df.iterrows():

    for age in range(int(row["Bracket Start Age"]), int(row["Bracket End Age"]) + 1):
        birth_years.append(2025 - age)
        male_population.append(row["Male"] / 5)
        female_population.append(row["Female"] / 5)

birth_year_population_df = pd.DataFrame(
    data={"year": birth_years, "male": male_population, "female": female_population}
)

birth_year_population_df = birth_year_population_df[
    birth_year_population_df["year"] < 2025
]

birth_year_population_df["male_prob"] = (
    birth_year_population_df["male"] / birth_year_population_df["male"].sum()
)
birth_year_population_df["female_prob"] = (
    birth_year_population_df["female"] / birth_year_population_df["female"].sum()
)

# %%
# names_genders = [
#     ("Megan", "female"),
#     ("Alexis", "female"),
#     # ("Cayenne", "female"),
# ]
names_genders = [
    ("Spencer", "male"),
    # ("Benjamin", "male"),
    # ("Garrett", "male"),
]
# names_genders = [
#     ("John", "male"),
#     ("Mackenzie", "female"),
# ]

# names_genders = [
#     ("Cynthia", "female"),
#     ("Michelle", "female"),
#     ("Christina", "female"),
# ]
# names_genders = [
#     ("Alex", "male"),
#     ("Rachel", "female"),
#     ("Elizabeth", "female"),
# ]


def get_name_df(name, selected_df):
    name_df = pd.DataFrame(selected_df.loc[name].iloc[-99:]).reset_index(names="year")
    name_df[f"{name}_prob"] = name_df[name] / name_df[name].sum()

    name_df["year"] = name_df["year"].astype("Int64")

    return name_df


all_name_dfs = []
for name, gender in names_genders:
    if gender == "male":
        selected_df = male_df
    else:
        selected_df = female_df

    curr_name_df = get_name_df(name, selected_df)

    all_name_dfs.append(curr_name_df)

name_df = reduce(
    lambda left, right: pd.merge(left, right, on="year", how="inner"), all_name_dfs
)


combined_df = birth_year_population_df.merge(name_df, on="year", how="inner")
combined_df["combined_probability"] = combined_df[
    [f"{name}_prob" for name, _ in names_genders] + ["male_prob"]  # , "female_prob"]
].prod(axis=1)

combined_df["combined_probability"] = (
    combined_df["combined_probability"] / combined_df["combined_probability"].sum()
)

fig = go.Figure()
# fig.add_trace(
#     go.Scatter(
#         x=combined_df["year"],
#         y=combined_df[f"{gender}_prob"],
#         name="Population Pyramid",
#     )
# )

for name, _ in names_genders:
    fig.add_trace(
        go.Scatter(x=combined_df["year"], y=combined_df[f"{name}_prob"], name=name)
    )
fig.add_trace(
    go.Scatter(
        x=combined_df["year"],
        y=combined_df[f"combined_probability"],
        name="Combined Probability",
    )
)

fig.show()


most_common_idx = combined_df["combined_probability"].idxmax()
print(combined_df.loc[most_common_idx]["year"])

expected_value = (combined_df["year"] * combined_df["combined_probability"]).sum()
print(expected_value)

sd = np.sqrt(
    (
        np.pow((combined_df["year"] - expected_value), 2)
        * combined_df["combined_probability"]
    ).sum()
)

print(sd)
# %%
