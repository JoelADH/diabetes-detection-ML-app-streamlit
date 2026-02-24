import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

DATA_PATH = "data/diabetes_binary_health_indicators_BRFSS2015.csv"
TARGET_COL = "Diabetes_binary"
MODEL_OUT_PATH = "models/best_model.pkl"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def render():
    st.title("Model training and evaluation")

    df = load_data()
   
    if "results_df" not in st.session_state:
        st.session_state.results_df = None
    if "diagnostics" not in st.session_state:
        st.session_state.diagnostics = None
    if "trained" not in st.session_state:
        st.session_state.trained = False
    
    st.subheader("Train/test split")

    test_size = st.slider("Test size proportion", 0.1, 0.4, 0.2, 0.05)

    X_train, X_test, y_train, y_test = split_data(df, test_size=test_size)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Training samples", len(X_train))
    with col2:
        st.metric("Test samples", len(X_test))
    with col3:
        st.metric("Number of features", X_train.shape[1])

    st.caption("Stratified split applied to preserve class distribution.")

    st.subheader("Model Training")

    use_balanced = st.checkbox(
        "Use class_weight='balanced' to address class imbalance",
        value=True
    )

    if st.button("Train and Evaluate Models"):
        with st.spinner("Training models, please wait."):
            models = train_models(X_train, y_train, balanced=use_balanced)

            results = []
            diagnostics = {}

            for name, model in models.items():
                metrics, cm, report = evaluate_model(
                    model, X_train, y_train, X_test, y_test
                )

                row = {"Model": name, **metrics}
                results.append(row)
                diagnostics[name] = {"model": model, "cm": cm, "report": report}

            st.session_state.results_df = pd.DataFrame(results).set_index("Model")
            st.session_state.diagnostics = diagnostics
            st.session_state.trained = True

    if st.session_state.trained:

        results_df = st.session_state.results_df
        diagnostics = st.session_state.diagnostics

        st.subheader("Test Performance Comparison")

        st.dataframe(
            results_df.sort_values("f1_score", ascending=False),
            use_container_width=True
        )

        st.info(
            "In imbalanced classification problems, Recall and F1-score "
            "are often more informative than Accuracy."
        )

        metric_choice = st.selectbox(
            "Select metric to determine best model:",
            ["f1_score", "recall", "roc_auc", "test_accuracy"],
            index=0
        )

        best_row = results_df.sort_values(metric_choice, ascending=False).iloc[0]
        best_model_name = best_row.name

        st.success(f"Best model according to {metric_choice}: {best_model_name}")

        st.subheader("Diagnostic Report")

        st.write("Confusion Matrix (Test Set):")
        cm = diagnostics[best_model_name]["cm"]
        plot_confusion_matrix(cm)
        # st.write(pd.DataFrame(
        #     cm,
        #     index=["Actual 0", "Actual 1"],
        #     columns=["Predicted 0", "Predicted 1"]
        # ))

        st.write("Classification Report:")
        st.code(diagnostics[best_model_name]["report"])

        st.subheader("Save Model for Deployment")

        if st.button("Save Best Model"):
            st.session_state.best_model = diagnostics[best_model_name]["model"]
            st.session_state.feature_columns = X_train.columns.tolist()
            st.session_state.best_model_name = best_model_name

            st.success("Model stored in session. Go to 'demo' in the sidebar to use it.")
            st.caption("The model is kept in memory for the current app session.")

        
        if st.button("Reset Results"):
            st.session_state.results_df = None
            st.session_state.diagnostics = None
            st.session_state.trained = False


def split_data(df, test_size=0.2, random_state=42):
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )

    return X_train, X_test, y_train, y_test


def train_models(X_train, y_train, balanced=False, random_state=42):

    class_weight = "balanced" if balanced else None

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=2000,
            class_weight=class_weight,
            random_state=random_state
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=5,
            min_samples_leaf=50,
            min_samples_split=200,
            class_weight=class_weight,
            random_state=random_state
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=400,
            max_depth=12,
            min_samples_leaf=50,
            min_samples_split=200,
            class_weight=class_weight,
            random_state=random_state,
            n_jobs=-1
        )
    }

    for model in models.values():
        model.fit(X_train, y_train)

    return models


def evaluate_model(model, X_train, y_train, X_test, y_test):

    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    y_proba_test = None
    if hasattr(model, "predict_proba"):
        y_proba_test = model.predict_proba(X_test)[:, 1]

    metrics = {
        "train_accuracy": accuracy_score(y_train, y_pred_train),
        "test_accuracy": accuracy_score(y_test, y_pred_test),
        "precision": precision_score(y_test, y_pred_test, zero_division=0),
        "recall": recall_score(y_test, y_pred_test, zero_division=0),
        "f1_score": f1_score(y_test, y_pred_test, zero_division=0),
    }

    if y_proba_test is not None:
        metrics["roc_auc"] = roc_auc_score(y_test, y_proba_test)
    else:
        metrics["roc_auc"] = np.nan

    cm = confusion_matrix(y_test, y_pred_test)
    report = classification_report(y_test, y_pred_test, zero_division=0)

    return metrics, cm, report


def select_best_model(results_df, metric="f1_score"):
    return results_df.sort_values(by=metric, ascending=False).iloc[0]



def plot_confusion_matrix(cm):
    fig, ax = plt.subplots(figsize=(6, 5))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        linewidths=0.5,
        linecolor="gray",
        ax=ax
    )

    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("Actual Label")
    ax.set_title("Confusion Matrix")

    ax.set_xticklabels(["No Diabetes", "Diabetes"])
    ax.set_yticklabels(["No Diabetes", "Diabetes"], rotation=0)

    plt.tight_layout()

    st.pyplot(fig)