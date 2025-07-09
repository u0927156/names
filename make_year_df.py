# %%
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

# %%
names_col = ["name", "gender", "count"]
names_2023_df = pd.read_csv("./name_data/yob2023.txt", header=None)
names_2023_df.columns = names_col
# %%
top_2000_names_df = names_2023_df.iloc[:2000, :]

# %%

name_data_path = Path("./name_data")


def get_year_names_of_gender_with_at_least_n(
    df: pd.DataFrame, gender: str, n: int, year: int
):
    gender_df = df.query(f"gender == '{gender}' & count >= {n}")
    return (
        gender_df.set_index("name")
        .drop(columns=["gender"])
        .rename(columns={"count": year})
    )


f_df_list = []
m_df_list = []
for text_file in name_data_path.glob("*.txt"):
    year = int(str(text_file).split(".")[0][-4:])

    year_df = pd.read_csv(text_file, header=None)
    year_df.columns = names_col

    f_names_df = get_year_names_of_gender_with_at_least_n(year_df, "F", 5, year)
    f_df_list.append(f_names_df)

    m_names_df = get_year_names_of_gender_with_at_least_n(year_df, "M", 5, year)
    m_df_list.append(m_names_df)
    # total_num_babies_born_this_year = year_df.count.sum()
    # leigh_count = year_df[year_df.name.str.endswith("leigh")]["count"].sum() / total_num_babies_born_this_year
    # lynn_counts.append(year_df[year_df.name.str.endswith("lynn")]["count"].sum() / total_num_babies_born_this_year)

    # leigh_counts.append(leigh_count)
    # years.append(year)

# %%


def merge_list_of_dataframes_on_index(list_of_dfs):
    df: pd.DataFrame = list_of_dfs[0]

    for other_df in list_of_dfs[1:]:
        df = df.merge(other_df, left_index=True, right_index=True, how="outer")

    df = df.fillna(0)
    return df


merged_f_df = merge_list_of_dataframes_on_index(f_df_list)
merged_m_df = merge_list_of_dataframes_on_index(m_df_list)

output_data_path = Path("./processed_data")
merged_f_df.to_csv(output_data_path / "female_names.csv")
merged_m_df.to_csv(output_data_path / "male_names.csv")
# %%
