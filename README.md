# Machine Learning Project: A diabetes risk prediction app 

An interactive Streamlit application for exploring, training, and evaluating machine learning models to predict diabetes risk using health indicators from the [BRFSS 2015 dataset](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators).

This project includes a machine learning workflow:

- Exploratory Data Analysis (EDA).
- Handling imbalanced classification.
- Model training and evaluation.
- Interactive prediction demo.
- Interpretation and conclusions.
- Basic ML deployment using Streamlit.

## Web application demo

Click on this button to access the web application and give it a try!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://diabetes-detection-ml-app.streamlit.app/)

## Application sections

The app is organized into the following sections:

- **Introduction** : Project overview and objectives.  
- **Dataset Report** : Dataset structure and summary statistics. 
- **EDA** : Exploratory Data Analysis with visualizations.  
- **Models** : Training, evaluation, and model comparison.  
- **Demo** : Interactive diabetes risk prediction.  
- **Conclusions** : Key findings, limitations, and future work.  

## Dataset

The project uses the **Behavioral Risk Factor Surveillance System (BRFSS) 2015** dataset.

This dataset contains health-related survey indicators such as:

- BMI
- Age category
- General health
- Lifestyle factors
- Cardiovascular history
- Socioeconomic indicators

Target variable: **Diabetes_binary**

Binary classification:
- `0` → Non-diabetic  
- `1` → Diabetic  

## Machine learning models

The following models were implemented and compared:

- Logistic Regression  
- Decision Tree (regularized)  
- Random Forest (regularized)  

Evaluation metrics:

- Accuracy  
- Precision  
- Recall  
- F1-score  
- ROC-AUC  

Given the medical screening context, Recall and ROC-AUC were prioritized over Accuracy.

The app also allows adjusting the decision threshold in the demo part to explore sensitivity and specificity trade-offs.

## Run the app

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

## Learning context

This project was developed as part of a Machine Learning Introduction Microcredential provided by [La Laguna University](https://www.ull.es/).

## Disclaimer

**This application is an educational prototype and does not provide medical diagnosis. Always consult healthcare professionals for medical advice.**