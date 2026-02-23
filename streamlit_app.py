import streamlit as st

# st.title("🎈 My new app")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )

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


