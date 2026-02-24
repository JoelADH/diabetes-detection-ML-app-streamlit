import streamlit as st

def render():
    st.title("Conclusions")
    st.markdown("## Executive Summary")

    st.success(
        """
        **This project built an end-to-end diabetes risk screening prototype** using BRFSS 2015 survey indicators.
        The workflow included **EDA, model training with class imbalance handling**, and an **interactive prediction demo**.
        The final models achieved **stable generalization** (Train ≈ Test) with **ROC-AUC around ~0.82**.
        """
    )

    st.markdown("---")
    st.markdown("## Key Findings")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            """
            **Dataset insights**
            - Binary classification: *Diabetes_binary* (0/1)
            - **Imbalanced target**
            - Survey-based (self-reported) features
            """
        )

    with col2:
        st.info(
            """
            **EDA patterns**
            - Higher **BMI** : higher risk
            - Higher **Age group** : higher risk
            - Poorer **General Health** : higher risk
            """
        )

    with col3:
        st.info(
            """
            **Correlation**
            - Correlations are **moderate** (expected in health data)
            - Useful for **feature prioritization**
            - Not causal evidence
            """
        )

    st.markdown("---")
    st.markdown("## Model Performance Summary")

    col4, col5 = st.columns(2)

    with col4:
        st.success(
            """
            **What worked best**
            - Regularization reduced tree overfitting (Train ≈ Test)
            - Logistic Regression and Random Forest performed similarly
            - **ROC-AUC ~0.82** indicates good ranking ability
            """
        )

    with col5:
        st.warning(
            """
            **Metric selection matters**
            - **Accuracy alone is misleading** under imbalance
            - Screening use case : prioritize **Recall**
            - Trade-off: higher Recall usually reduces Precision
            """
        )

    st.markdown("---")
    st.markdown("## Thresholding and Trade-offs")

    st.write(
        """
        Many classifiers output a probability (risk score). A **decision threshold** converts that probability into a class:
        - Lower threshold : **more positives detected** (higher Recall) but more false positives (lower Precision)
        - Higher threshold : fewer false positives but **more missed cases**
        
        In medical screening contexts, the cost of missing true cases is often high, so **Recall is usually prioritized**.
        """
    )

    st.markdown("---")
    st.markdown("## Final Recommendation")

    st.info(
        """
        **Recommended approach for this prototype:**
        - Use the best model according to **Recall , F1 , ROC-AUC** depending on the goal.
        - For screening, deploy with an adjustable **threshold** to tune sensitivity.
        - Always communicate that this tool is **not a medical diagnosis**.
        """
    )

    st.markdown("---")
    st.markdown("## Limitations")

    col6, col7 = st.columns(2)

    with col6:
        st.write(
            """
            **Data limitations**
            - Self-reported (survey) variables can be noisy
            - No lab biomarkers (e.g., glucose, HbA1c)
            - Dataset is from **2015**, may not reflect current patterns
            """
        )

    with col7:
        st.write(
            """
            **Model limitations**
            - No external validation cohort
            - Threshold tuning affects false positives/negatives
            - Correlation-based feature ranking is limited for non-linear relationships
            """
        )

    st.markdown("---")

    st.caption(
        "Disclaimer: This application is an educational prototype and does not provide medical diagnosis."
    )