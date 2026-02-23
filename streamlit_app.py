import streamlit as st
from views import dataset_report, intro, eda
st.set_page_config(
    page_title = "Diabetes risk prediction App",
    layout="wide"
)

st.sidebar.title("Navegación")

section = st.sidebar.radio(
    "Go to:",
    (
        "Introduction",
        "dataset report",
        "EDA",
        "models",
        "demo",
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

if section == "dataset report":
    dataset_report.render()

if section == "EDA":
    eda.render()
