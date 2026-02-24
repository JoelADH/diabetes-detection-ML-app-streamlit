import streamlit as st
import pandas as pd

AGE_MAP = {
    "18–24 (1)": 1,
    "25–29 (2)": 2,
    "30–34 (3)": 3,
    "35–39 (4)": 4,
    "40–44 (5)": 5,
    "45–49 (6)": 6,
    "50–54 (7)": 7,
    "55–59 (8)": 8,
    "60–64 (9)": 9,
    "65–69 (10)": 10,
    "70–74 (11)": 11,
    "75–79 (12)": 12,
    "80+ (13)": 13,
}

EDUCATION_MAP = {
    "Never attended school / Kindergarten only (1)": 1,
    "Grades 1–8 (2)": 2,
    "Grades 9–11 (3)": 3,
    "High school graduate (4)": 4,
    "Some college or technical school (5)": 5,
    "College graduate (6)": 6,
}

INCOME_MAP = {
    "< $10,000 (1)": 1,
    "$10,000–$15,000 (2)": 2,
    "$15,000–$20,000 (3)": 3,
    "$20,000–$25,000 (4)": 4,
    "$25,000–$35,000 (5)": 5,
    "$35,000–$50,000 (6)": 6,
    "$50,000–$75,000 (7)": 7,
    "≥ $75,000 (8)": 8,
}

def build_default_features(feature_cols):
    """Initialize all features to 0, so only fill what the user sets."""
    return {c: 0 for c in feature_cols}

def render():
    st.title("Demo: Diabetes Risk Prediction")

    if "best_model" not in st.session_state or "feature_columns" not in st.session_state:
        st.warning("No trained model found. Please go to the Models section, train models and click 'Save Best Model'.")
        return

    model = st.session_state.best_model
    feature_cols = st.session_state.feature_columns
    model_name = st.session_state.get("best_model_name", "Unknown")

    st.info(f"Using model: **{model_name}**")

    st.markdown(
        """
This is an **experimental screening tool** trained on BRFSS 2015 survey indicators.
It estimates diabetes risk from self-reported health factors and **does not provide a medical diagnosis**.
"""
    )

    st.sidebar.subheader("Decision threshold")
    threshold = st.sidebar.slider(
        "Classify as 'positive' (1) if probability ≥",
        min_value=0.05, max_value=0.95, value=0.50, step=0.05
    )
    st.sidebar.caption("Lower threshold → higher recall (more positives), but more false positives.")

   
    st.subheader("Patient / user inputs")

    with st.form("risk_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            bmi = st.number_input("BMI", min_value=10.0, max_value=80.0, value=27.0, step=0.5)
            age_label = st.selectbox(
                "Age group",
                list(AGE_MAP.keys()),
                index=6,
                help="Age is encoded as categories (1–13) in this dataset."
            )
            age_cat = AGE_MAP[age_label]
            genhlth = st.selectbox("General health (1=Excellent … 5=Poor)", [1, 2, 3, 4, 5], index=2)
            physactivity = st.selectbox("Physical activity in past 30 days?", ["Yes", "No"], index=0)

        with col2:
            highbp = st.selectbox("High blood pressure?", ["No", "Yes"], index=0)
            highchol = st.selectbox("High cholesterol?", ["No", "Yes"], index=0)
            cholcheck = st.selectbox("Cholesterol checked in last 5 years?", ["No", "Yes"], index=1)
            smoker = st.selectbox("Smoked ≥100 cigarettes in lifetime?", ["No", "Yes"], index=0)

        with col3:
            stroke = st.selectbox("History of stroke?", ["No", "Yes"], index=0)
            heartdisease = st.selectbox("Coronary heart disease / MI?", ["No", "Yes"], index=0)
            diffwalk = st.selectbox("Serious difficulty walking/climbing stairs?", ["No", "Yes"], index=0)
            fruits = st.selectbox("Consumes fruit ≥ 1/day?", ["No", "Yes"], index=1)
            veggies = st.selectbox("Consumes vegetables ≥ 1/day?", ["No", "Yes"], index=1)

        st.markdown("### Additional factors")
        col4, col5, col6 = st.columns(3)

        with col4:
            phys_hlth = st.slider("Physical health not good (days, last 30)", 0, 30, 0)
            ment_hlth = st.slider("Mental health not good (days, last 30)", 0, 30, 0)
            sleep_time = st.slider("Sleep time (hours)", 1, 24, 7)

        with col5:
            hvyalcohol = st.selectbox("Heavy alcohol consumption?", ["No", "Yes"], index=0)
            anyhealthcare = st.selectbox("Has any health care coverage?", ["No", "Yes"], index=1)
            nodocbcost = st.selectbox("Could not see doctor due to cost?", ["No", "Yes"], index=0)

        with col6:
            sex = st.selectbox("Sex", ["Female", "Male"], index=0)
            education_label = st.selectbox(
                "Education level",
                list(EDUCATION_MAP.keys()),
                index=4,
                help="Education is encoded as categories (1–6) in the dataset."
            )
            education = EDUCATION_MAP[education_label]
            income_label = st.selectbox(
                "Income level",
                list(INCOME_MAP.keys()),
                index=5,
                help="Income is encoded as categories (1–8) in the dataset."
            )
            income = INCOME_MAP[income_label]

        submitted = st.form_submit_button("Predict risk")

    if not submitted:
        return

    features = build_default_features(feature_cols)

    def set_if_exists(col, val):
        if col in features:
            features[col] = val

    set_if_exists("BMI", float(bmi))
    set_if_exists("Age", int(age_cat))
    set_if_exists("GenHlth", int(genhlth))
    set_if_exists("PhysHlth", int(phys_hlth))
    set_if_exists("MentHlth", int(ment_hlth))
    set_if_exists("SleepTime", int(sleep_time))
    set_if_exists("Education", int(education))
    set_if_exists("Income", int(income))

    yn = {"No": 0, "Yes": 1}
    set_if_exists("HighBP", yn[highbp])
    set_if_exists("HighChol", yn[highchol])
    set_if_exists("CholCheck", yn[cholcheck])
    set_if_exists("Smoker", yn[smoker])
    set_if_exists("Stroke", yn[stroke])
    set_if_exists("HeartDiseaseorAttack", yn[heartdisease])
    set_if_exists("DiffWalk", yn[diffwalk])
    set_if_exists("Fruits", yn[fruits])
    set_if_exists("Veggies", yn[veggies])
    set_if_exists("HvyAlcoholConsump", yn[hvyalcohol])
    set_if_exists("AnyHealthcare", yn[anyhealthcare])
    set_if_exists("NoDocbcCost", yn[nodocbcost])
    set_if_exists("PhysActivity", yn[physactivity])

    set_if_exists("Sex", 1 if sex == "Male" else 0)

    user_df = pd.DataFrame([features])[feature_cols]

    proba = None
    pred = int(model.predict(user_df)[0])

    if hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(user_df)[0, 1])
        pred = 1 if proba >= threshold else 0

    st.subheader("Result")

    if proba is not None:
        st.metric("Estimated probability (class 1)", f"{proba:.2%}")
        st.caption(f"Decision threshold: {threshold:.2f}")
    else:
        st.caption("This model does not support probability estimates.")

    if pred == 1:
        st.error("Prediction: **Higher risk (Positive)**")
    else:
        st.success("Prediction: **Lower risk (Negative)**")

    st.markdown(
        """
**Important:** This is not a diagnosis.  
If you have concerns, consult a healthcare professional.
"""
    )

    with st.expander("Show feature vector sent to the model"):
        st.dataframe(user_df, use_container_width=True)