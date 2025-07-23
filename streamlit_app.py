import streamlit as st
import pandas as pd
from pathlib import Path


from names.name_utils import convert_number_to_rate, add_sound_columns
from names.name_by_time import plot_name_popularity_by_time


st.write("# Name App+++")


pg = st.navigation(
    [
        st.Page("pages/Estimate_Age_By_Name.py"),
        st.Page(
            "pages/Name_Popularity.py",
        ),
        st.Page("pages/Top_Names_by_Year.py"),
    ]
)
pg.run()

st.markdown(
    """
### Credits
Written by Spencer Peterson

Data: 
- [CDC Birth Data](https://data.cdc.gov/National-Center-for-Health-Statistics/NCHS-Births-and-General-Fertility-Rates-United-Sta/e6fc-ccez/about_data)
- [2019](https://www.cdc.gov/nchs/data/nvsr/nvsr70/nvsr70-02-508.pdf)
- [2020](https://www.cdc.gov/nchs/data/vsrr/vsrr012-508.pdf)
- [2021-2022](https://www.cdc.gov/nchs/products/databriefs/db477.htm)
- [2023](https://www.cdc.gov/nchs/products/databriefs/db507.htm)
- [2024](https://www.cdc.gov/nchs/pressroom/nchs_press_releases/2025/20250423.htm)
- [Population Pyramid](https://www.census.gov/data-tools/demo/idb/#/dashboard?dashboard_page=country&COUNTRY_YR_ANIM=2025&COUNTRY_YEAR=2025&CCODE=US&menu=countryViz&CCODE_SINGLE=US&subnat_map_admin=ADM1)
            """
)
