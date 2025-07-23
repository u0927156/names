import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

from names.estimate_age import estimate_age
from names.name_utils import load_process_population_pyramid_df


name_data_path = Path("./processed_data")

female_df = pd.read_csv(name_data_path / "female_names.csv", index_col=0)
male_df = pd.read_csv(name_data_path / "male_names.csv", index_col=0)

birth_year_population_df = load_process_population_pyramid_df()

CURRENT_YEAR = 2025

st.markdown(
    """
            # Age Estimator
            This page can estimate a person's age based on their name. Enter a name below and their 
            gender to get an estimate of their name.    

            This is only using birth data from the United States, so the estimation will not be accurate for 
            people born abroad.

            ## Input

"""
)


selected_name = st.text_input("Search a Name:", value="Spencer")
gender = st.radio("Gender", options=["male", "female"], format_func=str.title)

st.markdown(
    """
            ### Friends
            You can improve the estimation by adding childhood friends or spouses.
            """
)

friends_df = st.data_editor(
    pd.DataFrame(columns=["Name", "Gender"]),
    num_rows="dynamic",
    column_config={
        "Name": st.column_config.TextColumn(
            "Name", max_chars=50, validate=r"^[A-Z]{1}[a-z]+"
        ),
        "Gender": st.column_config.SelectboxColumn(
            "Gender", options=["Male", "Female"]
        ),
    },
)

friend_tuples = list(friends_df.itertuples(index=False, name=None))
name_genders = [
    (selected_name, gender),
] + [
    (name, curr_gender.lower())
    for name, curr_gender in friend_tuples
    if name is not None and curr_gender is not None
]

try:
    common_year, average_year, std_year, combined_df = estimate_age(
        name_genders,
        male_df=male_df,
        female_df=female_df,
        birth_year_population_df=birth_year_population_df,
    )

    st.markdown("# Estimation")
    st.write(
        f"**This person's estimated age is {CURRENT_YEAR - round(average_year)} ± {round(std_year)} years. ({round(average_year)})**"
    )

    st.markdown(
        """
                ## Details
                
                The following charts show the probability of a person being born in a given year based on their name. Additionally,
                we have the probability of a person being born in a year based off of the US population pyramid.

                There are two charts below. The first shows the individual probability distributions for all of the predictors. 
                The second shows the combined probability that we use to estimate the age.

                To get the estimated age, we take the [expected value](https://en.wikipedia.org/wiki/Expected_value) of the combined probability distribution.
                """
    )
    fig = go.Figure()
    for name, _ in name_genders:
        fig.add_trace(
            go.Scatter(x=combined_df["year"], y=combined_df[f"{name}_prob"], name=name)
        )
    fig.add_trace(
        go.Scatter(
            x=combined_df["year"],
            y=combined_df[f"{gender}_prob"],
            name="Probability of Being Born in Year",
        )
    )

    fig.update_layout(
        title="Probability of Being Born in a Year by Name",
        xaxis_title="Year",
        yaxis_title="Probability",
    )

    st.plotly_chart(fig)

    combined_prob_fig = go.Figure()
    combined_prob_fig.add_trace(
        go.Scatter(
            x=combined_df["year"],
            y=combined_df[f"combined_probability"],
            name="Combined Probability",
        )
    )
    combined_prob_fig.update_layout(
        title="Combined Probability of Being Born in a Year",
        xaxis_title="Year",
        yaxis_title="Probability",
    )

    combined_prob_fig.add_vline(x=average_year, annotation=dict(text="Expected Year"))
    combined_prob_fig.add_vline(
        x=average_year + std_year,
        line_dash="dash",
        annotation=dict(text="+σ"),
    )
    combined_prob_fig.add_vline(
        x=average_year - std_year,
        line_dash="dash",
        annotation=dict(text="-σ"),
    )

    st.plotly_chart(combined_prob_fig)
except Exception as e:
    st.write(f"{e}")

st.write(
    "This was written in 2025. Because of the unceasing nature of time, age estimates may no longer be accurate."
)
