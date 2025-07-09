# %%
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import jellyfish
from names.name_utils import convert_number_to_rate

# %%
name_data_path = Path("./processed_data")

female_df = pd.read_csv(name_data_path / "female_names.csv", index_col=0)
male_df = pd.read_csv(name_data_path / "male_names.csv", index_col=0)

female_rate_df = convert_number_to_rate(female_df)
male_rate_df = convert_number_to_rate(male_df)

# %%


def add_sound_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["metaphone"] = [jellyfish.metaphone(name) for name in df.index]
    df["soundex"] = [jellyfish.soundex(name) for name in df.index]
    df["nysiis"] = [jellyfish.nysiis(name) for name in df.index]
    df["match_rating_codex"] = [jellyfish.match_rating_codex(name) for name in df.index]
    return df


male_df = add_sound_columns(male_df)
female_df = add_sound_columns(female_df)
female_rate_df = add_sound_columns(female_rate_df)
male_rate_df = add_sound_columns(male_rate_df)

# %%
female_df.groupby(
    ["metaphone", "soundex", "nysiis", "match_rating_codex"]
).size().sort_values(ascending=False)

# %%
female_df.query(
    "metaphone == 'LN' & soundex == 'L500' & nysiis == 'LAN' & match_rating_codex == 'LN'"
)

# %%


def plot_name_popularity_by_time(df, name, plot_related_names=False):
    if name not in df.index:
        print(f"{name} not found.")
        return None

    years = [col for col in df.columns if col.isnumeric()]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=years, y=df.loc[name][years], name=name, line=dict(width=5))
    )

    if plot_related_names:
        # Organize by total popularity
        sound_columns = ["metaphone", "soundex", "nysiis", "match_rating_codex"]
        name_information = df.loc[name]
        df["num_matches"] = df[sound_columns].apply(
            (
                lambda row: int(row["metaphone"] == name_information["metaphone"])
                + int(row["soundex"] == name_information["soundex"])
                + int(row["nysiis"] == name_information["nysiis"])
                + int(
                    row["match_rating_codex"] == name_information["match_rating_codex"]
                )
            ),
            axis=1,
        )

        names_with_same_code = df[df["num_matches"] >= 3].index
        names_with_same_code = [n for n in names_with_same_code if n != name]
        names_with_same_code = list(
            df.loc[names_with_same_code][years]
            .sum(axis=1)
            .sort_values(ascending=False)
            .index
        )
        for associated_name in names_with_same_code:
            fig.add_trace(
                go.Scatter(
                    x=years,
                    y=df.loc[associated_name][years],
                    name=associated_name,
                    line=dict(width=1),
                )
            )

    fig.update_layout(
        title=f"Popularity of {name} and Associated Names over Time",
        xaxis=dict(tickmode="linear", tick0=years[0], dtick=10),
        # yaxis_range=[0, 1],
    )

    return fig


name = "Vera"
fig = plot_name_popularity_by_time(female_rate_df, "Vera", True)
fig.show()
# %%
fig = plot_name_popularity_by_time(female_rate_df, "Vera", True)
fig.show()
# %%


def plot_history_of_top_n_names_from_year(df, n, year):
    years = [col for col in df.columns if col.isnumeric()]

    top_n_names = female_df[year].sort_values(ascending=False).index[0:n]

    x_years = [int(y) for y in years]
    fig = go.Figure()
    for name in top_n_names:
        fig.add_trace(go.Scatter(x=x_years, y=df.loc[name][years], name=name))

    print(year)
    fig.add_vline(
        x=int(year),
    )

    fig.update_layout(
        title=f"Popularity of the Top {n} Names from {year} over Time",
        xaxis=dict(tickmode="linear", tick0=x_years[0], dtick=10),
        # yaxis_range=[0, 1],
    )
    return fig


plot_history_of_top_n_names_from_year(female_df, 20, "1880")
