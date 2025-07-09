# %%
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

# %%
name_data_path = Path("./processed_data")

female_df = pd.read_csv(name_data_path / "female_names.csv", index_col=0)
male_df = pd.read_csv(name_data_path / "male_names.csv", index_col=0)


# %%
def find_proportion_of_top_n_names(df, n):
    years = []
    yearly_top_n_proportion = []
    for year in df.columns:
        total_names_for_year = df[year].sum()

        ranked_names = df[year].rank(ascending=False).sort_values()
        sum_of_top_n_names_year = df.loc[ranked_names[ranked_names <= n].index][
            year
        ].sum()

        top_n_proportion = sum_of_top_n_names_year / total_names_for_year
        # print(year, sum_of_top_50_names_year / total_names_for_year)

        years.append(year)
        yearly_top_n_proportion.append(top_n_proportion)

    return years, yearly_top_n_proportion


# %%
def compare_male_female_top_n_proportion(
    female_df: pd.DataFrame, male_df: pd.DataFrame, n: int
) -> go.Figure:
    years, female_top_n_proportion = find_proportion_of_top_n_names(female_df, n)
    _, male_top_n_proportion = find_proportion_of_top_n_names(male_df, n)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=years,
            y=female_top_n_proportion,
            name="Female",
            line=dict(color="pink", width=5),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=male_top_n_proportion,
            name="Male",
            line=dict(color="lightblue", width=5),
        )
    )

    fig.update_layout(
        title=f"Proportion of Top {n} Names over Time",
        xaxis=dict(tickmode="linear", tick0=years[0], dtick=10),
        yaxis_range=[0, 1],
    )

    return fig


compare_male_female_top_n_proportion(female_df=female_df, male_df=male_df, n=10)

# %%
compare_male_female_top_n_proportion(female_df=female_df, male_df=male_df, n=50)
# %%
compare_male_female_top_n_proportion(female_df=female_df, male_df=male_df, n=100)


# %%
