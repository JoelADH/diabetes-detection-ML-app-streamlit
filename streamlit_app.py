import streamlit as st
from views import dataset_report, intro, eda, models, demo, conclusions
st.set_page_config(
    page_title = "Diabetes risk prediction App",
    layout="wide"
)

st.sidebar.title("Sections")

section = st.sidebar.radio(
    "",
    (
        "Introduction",
        "Dataset report",
        "EDA",
        "Models",
        "Demo",
        "Conclusions"
    )
)

st.sidebar.markdown("---")
st.sidebar.info(
    "ML project applied to prediction of "
    "diabetes risk based on BRFSS 2015 dataset"
)

if section == "Introduction":
    intro.render()

if section == "Dataset report":
    dataset_report.render()

if section == "EDA":
    eda.render()

if section == "Models":
    models.render()

if section == "Demo":
    demo.render()

if section == "Conclusions":
    conclusions.render()