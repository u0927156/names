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
# The rise of leigh
name_data_path = Path("./name_data")

years = []
leigh_counts = []
lynn_counts = []
for text_file in name_data_path.glob("*.txt"):
    year = int(str(text_file).split(".")[0][-4:])

    year_df = pd.read_csv(text_file, header=None)
    year_df.columns = names_col

    total_num_babies_born_this_year = year_df["count"].sum()
    leigh_count = (
        year_df[year_df.name.str.endswith("leigh")]["count"].sum()
        / total_num_babies_born_this_year
    )
    lynn_counts.append(
        year_df[year_df.name.str.endswith("lynn")]["count"].sum()
        / total_num_babies_born_this_year
    )

    leigh_counts.append(leigh_count)
    years.append(year)


# %%

fig = go.Figure()

fig.add_trace(go.Scatter(x=years, y=leigh_counts, name="-leigh"))
fig.add_trace(go.Scatter(x=years, y=lynn_counts, name="-lynn"))

fig.show()
# %%
