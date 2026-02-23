import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

DATA_PATH = "data/diabetes_binary_health_indicators_BRFSS2015.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def render():
    st.title("Exploratory Data Analysis")

    df = load_data()

    column1, column2 = st.columns(2)

    with column1:
        plot_target_distribution(df)
    with column2:
        plot_target_pie(df)
  

    labels=["non-Diabetic","Diabetic"]
    plt.pie(df["Diabetes_binary"].value_counts() , labels =labels ,autopct='%.02f' );

    st.write("classes proportion:")
    st.write(df["Diabetes_binary"].value_counts(normalize=True))

    st.markdown("---")

    plot_hist_select_vars(df)

    st.markdown("---")
    plot_boxplots_global(df)
    plot_boxplots(df)

    st.markdown("---")
    plot_correlation_matrix(df)
    plot_corr_with_target(df)



def plot_target_distribution(df):
    st.subheader("Target variable distribution")

    target_counts = df["Diabetes_binary"].value_counts()
    fig, ax = plt.subplots()
    colors = ["#4185BD", "#8FDF61"]
    sns.barplot(
        x=target_counts.index, 
        y=target_counts.values, 
        palette=colors,
        ax=ax
    )
    ax.set_title("target variable count")
    ax.set_xlabel("Class (0 = Non-diabetic, 1 = Diabetic)")
    ax.set_ylabel("Frecuency")

    st.pyplot(fig)

def plot_target_pie(df):

    labels = ["Non-Diabetic", "Diabetic"]
    colors = ["#4185BD", "#8FDF61"]

    fig, ax = plt.subplots()

    ax.pie(
        df["Diabetes_binary"].value_counts(),
        labels=labels,
        autopct="%.02f%%",
        colors=colors,
        startangle=90
    )

    ax.set_title("class proportion")

    st.pyplot(fig)

def plot_hist_select_vars(df):
    st.subheader("Variables distribution")
    #numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    selected_hist_cols = ['BMI', 'GenHlth', 'MentHlth', 'PhysHlth', 'Age','Education', 'Income']

    n = len(selected_hist_cols)
    ncols = 2
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 6))
    axes = axes.flatten()

    for i, col in enumerate(selected_hist_cols):
        sns.histplot(df[col], kde=True, ax=axes[i])
        axes[i].set_title(col)

    
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")

    plt.tight_layout()
    st.pyplot(fig) 


def plot_boxplots_global(df):
    st.subheader("Boxplots per class. Outliers detection")
    cols = ["BMI", "GenHlth", "MentHlth", "PhysHlth", "Age", "Education", "Income"]

    fig, axes = plt.subplots(4,2, figsize=(10,10))
    axes = axes.flatten()

    for i, col in enumerate(cols):
        sns.boxplot(x=df[col], ax=axes[i])
        axes[i].set_title(col)

    plt.tight_layout()
    st.pyplot(fig)    

def plot_boxplots(df):

    selected_cols = ["BMI", "GenHlth", "MentHlth", "PhysHlth", "Age", "Education", "Income"]

    n = len(selected_cols)
    ncols = 2
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10,8))
    axes = axes.flatten()
    
    for i, col in enumerate(selected_cols):
        sns.boxplot(
            x="Diabetes_binary",
            y=col,
            data=df,
            ax=axes[i]
        )
        axes[i].set_title(col)

    for j in range(i+1, len(axes)):
        axes[j].axis("off")

    plt.tight_layout()
    st.pyplot(fig)


def plot_correlation_matrix(df):

    st.subheader("correlation matrix")

    corr = df.corr()

    fig, ax = plt.subplots(figsize = (25,10))

    sns.heatmap(
        corr,
        annot=True,
        cmap="YlOrRd",
        annot_kws={"size": 6},
        ax=ax,
        square=True,
        cbar=True
    )

    ax.set_title("Correlation Matrix")

    st.pyplot(fig)

def plot_corr_with_target(df):

    st.subheader("target correlation matrix")

    corr = df.corr()
    corr_target = corr["Diabetes_binary"].sort_values()

    fig, ax = plt.subplots(figsize=(6,8))
    corr_target.plot(kind="barh", ax=ax)

    ax.set_title("Diabetes_binary correlation")

    st.pyplot(fig)