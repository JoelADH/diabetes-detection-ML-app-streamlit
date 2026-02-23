import streamlit as st

def render():
    st.title("Diabetes risk prediction app")
    st.caption("ML + health project using BRFSS 2015 dataset")

    st.markdown(
        """
        ### Context
        Diabetes is a highly prevalent chronic disease associated with serious complications.
        The objective of this project is to **estimate the risk of diabetes** based on health 
        indicators and habits reported in population surveys.

        ### What's in this app?
        - **EDA:** Exploration and visualization of variables, distribution of classes and patterns.
        - **Modeling:** Training and comparison of classification models, including imbalance treatment.
        - **Prediction Demo:** Risk simulation for a user-entered profile.
        - **Conclusions:** findings, limitations and possible improvements.

        ### Dataset
        The dataset **BRFSS 2015** (Behavioral Risk Factor Surveillance System) is used, version:
        - *diabetes_binary_health_indicators_BRFSS2015.csv*
        - **binary** problem: *Diabetes_binary* (0 = no diabetes, 1 = prediabetes or diabetes)
        - **unbalanced dataset** for realistic purposes.
    
        ### Important Considerations
        - This tool is **educational and experimental**.
        - It **does not replace** medical diagnosis or clinical advice.
        - The result should be interpreted as a **statistical estimate** based on historical data.
        """
    )

    st.markdown("---")
    column1, column2, column3 = st.columns(3)

    with column1:
        st.metric("Type of problem", "Classification")
    with column2:
        st.metric("Target", "Diabetes_binary")
    with column3:
        st.metric("Approach", "Population risk")

    st.info(
        "Visit EDA section for better understanding of the data before " 
        "checking ML models or demo usage."
    )