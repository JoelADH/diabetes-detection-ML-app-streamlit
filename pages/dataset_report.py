import streamlit as st
import pandas as pd
import io

DATA_PATH = "data/diabetes_binary_health_indicators_BRFSS2015.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def render():
    st.title("Dataset report")

    df = load_data()

    st.subheader("DataSet info")

    st.markdown(
        """
##### About Columns :
- **Diabetes_binary** : you have diabetes (0,1)

- **HighBP** : Adults who have been told they have high blood pressure by a doctor, nurse, or other health professional (0,1)

- **HighChol** : Have you EVER been told by a doctor, nurse or other health professional that your blood cholesterol is high? (0,1)

- **CholCheck** : Cholesterol check within past five years (0,1)

- **BMI** : Body Mass Index (BMI)

- **Smoker** : Have you smoked at least 100 cigarettes in your entire life? [Note: 5 packs = 100 cigarettes] (0,1)

- **Stroke** : (Ever told) you had a stroke. (0,1)

- **HeartDiseaseorAttack** : Respondents that have ever reported having coronary heart disease (CHD) or myocardial infarction (MI) (0,1)

- **PhysActivity** : Adults who reported doing physical activity or exercise during the past 30 days other than their regular job (0,1)

- **Fruits** : Consume Fruit 1 or more times per day (0,1)

- **Veggies** : Consume Vegetables 1 or more times per day (0,1)

- **HvyAlcoholConsump** : Heavy drinkers (adult men having more than 14 drinks per week and adult women having more than 7 drinks per week)(0,1)

- **AnyHealthcare** : Do you have any kind of health care coverage, including health insurance, prepaid plans such as HMOs, or government plans such as Medicare, or Indian Health Service? (0,1)

- **NoDocbcCost** : Was there a time in the past 12 months when you needed to see a doctor but could not because of cost? (0,1)

- **GenHlth** : Would you say that in general your health is: rate (1 ~ 5)

- **MentHlth** : Now thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health not good? (0 ~ 30)

- **PhysHlth** : Now thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good? (0 ~ 30)

- **DiffWalk** : Do you have serious difficulty walking or climbing stairs? (0,1)

- **Sex** : Indicate sex of respondent (0,1) (Female or Male)

- **Age** : Fourteen-level age category (1 ~ 13)

- **Education** : What is the highest grade or year of school you completed? (1 ~ 6)

- **Income** : Is your annual household income from all sources: (If respondent refuses at any income level, code "Refused.") (1 ~ 8)
        """
    )

    st.markdown("---")
    
    column1, column2 = st.columns(2)

    with column1:
        st.markdown(
            """
            ##### Basic info, pandas pd.info() method
            """
        )
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text(info_str)
    with column2:
        st.markdown(
            """
            ##### DataSet shape
            """
        )
        rows, cols = df.shape
        st.write("Number of rows: ", rows, "Number of columns: ",cols)

    st.markdown(
            """
            ##### null values per column
            """
    )
    st.write(df.isnull().sum())

    st.markdown(
            """
            ##### Some of the data displayed
            """
    )
    st.write(style_df_head(df))

    st.markdown(
            """
            ##### Data describe
            """
    )
    st.write(df.describe().T)





def style_df_head(df):
    styled_df = df.head(5).T.style

    styled_df.set_properties(**{"background-color": "#D3EDD3", "color": "#000000", "border": "1.5px solid black"})

    styled_df.set_table_styles([
    {"selector": "th", "props": [("color", 'white'), ("background-color", "#333333")]}
    ])
    return styled_df