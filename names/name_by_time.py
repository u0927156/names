import plotly.graph_objects as go
import pandas as pd


def plot_name_popularity_by_time(
    df: pd.DataFrame, name: str, plot_related_names: bool = False
):
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

    title_str = (
        f"Popularity of {name}"
        + (" and Associated Names" if plot_related_names else "")
        + " over Time"
    )
    fig.update_layout(
        title=title_str,
        xaxis=dict(tickmode="linear", tick0=years[0], dtick=10),
        xaxis_title="Year",
    )

    return fig


def plot_history_of_top_n_names_from_year(df, n, year):
    years = [col for col in df.columns if col.isnumeric()]

    top_n_names = df[year].sort_values(ascending=False).index[0:n]

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
        xaxis_title="Year",
    )
    return fig
