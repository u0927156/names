import pandas as pd
import jellyfish


def convert_number_to_rate(df):

    return df.div(df.sum(axis=0), axis=1)


def add_sound_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["metaphone"] = [jellyfish.metaphone(name) for name in df.index]
    df["soundex"] = [jellyfish.soundex(name) for name in df.index]
    df["nysiis"] = [jellyfish.nysiis(name) for name in df.index]
    df["match_rating_codex"] = [jellyfish.match_rating_codex(name) for name in df.index]
    return df


def load_process_population_pyramid_df(
    file_loc="birth_data/United_States_(2025)_07-22-2025_1058_AM.csv",
):
    population_pyramid_df = pd.read_csv(file_loc)
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

        for age in range(
            int(row["Bracket Start Age"]), int(row["Bracket End Age"]) + 1
        ):
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

    return birth_year_population_df
