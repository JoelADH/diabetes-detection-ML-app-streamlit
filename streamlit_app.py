import streamlit as st
from pages import dataset_report, intro
st.set_page_config(
    page_title = "Diabetes risk prediction App",
    layout="wide"
)

st.sidebar.title("Navegación")

section = st.sidebar.radio(
    "Ir a:",
    (
        "Introduction",
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

if section == "EDA":
    dataset_report.render()

