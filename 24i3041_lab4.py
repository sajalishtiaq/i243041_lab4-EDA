# Part 1
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Part 2
st.set_page_config(page_title="EDA Explorer",page_icon="📊",layout="wide")

# Part 3
st.markdown("""
<style>
.stApp{
background:#FFFFFF;
color:#1F3258;
}
.main .block-container{
max-width:1200px;
padding-top:2rem;
padding-bottom:3rem;
}
[data-testid="stSidebar"]{
background:#1F3258;
padding-top:1rem;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span{
color:#FFFFFF;
}
[data-testid="stSidebar"] hr{
border-color:#467B85;
}
[data-testid="stSidebar"] .stButton button{
background:#467B85;
color:#FFFFFF;
border:none;
border-radius:8px;
font-weight:600;
}
[data-testid="stSidebar"] .stButton button:hover{
background:#FFFFFF;
color:#1F3258;
}
.hero{
background:#1F3258;
padding:2rem;
border-radius:14px;
margin-bottom:2rem;
}
.hero h1{
color:#FFFFFF;
margin:0;
font-size:2.3rem;
}
.hero p{
color:#FFFFFF;
opacity:0.8;
margin-top:0.5rem;
margin-bottom:0;
}
.section-title{
color:#1F3258;
font-size:1.4rem;
font-weight:700;
margin-top:1.5rem;
margin-bottom:0.8rem;
}
div[data-testid="stMetric"]{
background:#FFFFFF;
border:1px solid #E5E7EB;
border-left:5px solid #467B85;
padding:1rem;
border-radius:10px;
box-shadow:0 4px 12px rgba(31,50,88,0.08);
}
div[data-testid="stMetricLabel"]{
color:#467B85;
font-weight:600;
}
div[data-testid="stMetricValue"]{
color:#1F3258;
}
[data-testid="stDataFrame"]{
border:1px solid #E5E7EB;
border-radius:10px;
overflow:hidden;
}
.stSelectbox label{
color:#FFFFFF!important;
font-weight:600;
}
.stAlert{
border-radius:10px;
}
</style>
""",unsafe_allow_html=True)

# Part 4
st.sidebar.markdown("# EDA Explorer")
st.sidebar.markdown("---")
st.sidebar.write("Upload a CSV dataset and explore its structure, attributes, and patterns.")

uploaded_file=st.sidebar.file_uploader("Upload CSV Dataset",type=["csv"])

# Part 5
if uploaded_file is not None:
    try:
        df=pd.read_csv(
            uploaded_file,
            sep=None,
            engine="python",
            encoding_errors="replace"
        )
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.stop()

    if df.empty:
        st.error("The uploaded CSV file is empty.")
        st.stop()

    # Part 6
    st.markdown("""
    <div class="hero">
        <h1>Exploratory Data Analysis</h1>
        <p>Explore your dataset, inspect its structure, and discover visual patterns.</p>
    </div>
    """,unsafe_allow_html=True)

    # Part 7
    st.markdown('<div class="section-title">Dataset Preview</div>',unsafe_allow_html=True)
    st.dataframe(df.head(),use_container_width=True)

    # Part 8
    st.markdown('<div class="section-title">Dataset Overview</div>',unsafe_allow_html=True)

    col1,col2=st.columns(2)

    with col1:
        st.metric("Total Rows",df.shape[0])

    with col2:
        st.metric("Total Columns",df.shape[1])

    # Part 9
    st.markdown('<div class="section-title">Metadata Inspection</div>',unsafe_allow_html=True)

    metadata1,metadata2=st.columns(2)

    with metadata1:
        st.markdown("#### Column Data Types")

        data_types=pd.DataFrame({
            "Column":df.columns,
            "Data Type":df.dtypes.astype(str).values
        })

        st.dataframe(data_types,use_container_width=True)

    with metadata2:
        st.markdown("#### Missing Values")

        missing=pd.DataFrame({
            "Column":df.columns,
            "Missing Values":df.isnull().sum().values
        })

        st.dataframe(missing,use_container_width=True)

    # Part 10
    st.markdown('<div class="section-title">Numerical Statistical Summary</div>',unsafe_allow_html=True)

    numerical_columns=df.select_dtypes(include="number").columns

    if len(numerical_columns)>0:

        statistics=pd.DataFrame({
            "Mean":df[numerical_columns].mean(),
            "Median":df[numerical_columns].median(),
            "Minimum":df[numerical_columns].min(),
            "Maximum":df[numerical_columns].max()
        })

        st.dataframe(statistics,use_container_width=True)

    else:
        st.info("No numerical attributes found in this dataset.")

    # Part 11
    st.sidebar.markdown("---")
    st.sidebar.subheader("Attribute Analysis")

    selected_column=st.sidebar.selectbox(
        "Choose an Attribute",
        df.columns
    )

    # Part 12
    st.markdown('<div class="section-title">Data Visualization</div>',unsafe_allow_html=True)
    st.markdown(f"### {selected_column}")

    if pd.api.types.is_numeric_dtype(df[selected_column]):

        st.info("Numerical Attribute")

        data=df[selected_column].dropna()

        fig,ax=plt.subplots(figsize=(10,5))

        ax.hist(
            data,
            bins=20,
            color="#467B85",
            edgecolor="#FFFFFF",
            linewidth=1
        )

        ax.set_title(
            f"Distribution of {selected_column}",
            fontsize=16,
            fontweight="bold",
            color="#1F3258"
        )

        ax.set_xlabel(selected_column,color="#1F3258")
        ax.set_ylabel("Frequency",color="#1F3258")

        ax.tick_params(colors="#1F3258")

        ax.grid(
            axis="y",
            alpha=0.15
        )

        st.pyplot(fig)

    else:

        st.info("Categorical Attribute")

        counts=df[selected_column].dropna().value_counts()

        fig,ax=plt.subplots(figsize=(10,5))

        bars=ax.bar(
            counts.index.astype(str),
            counts.values,
            color="#467B85"
        )

        ax.set_title(
            f"Frequency Distribution of {selected_column}",
            fontsize=16,
            fontweight="bold",
            color="#1F3258"
        )

        ax.set_xlabel(selected_column,color="#1F3258")
        ax.set_ylabel("Frequency",color="#1F3258")

        ax.tick_params(
            axis="both",
            colors="#1F3258"
        )

        plt.xticks(rotation=45)

        ax.grid(
            axis="y",
            alpha=0.15
        )

        for bar,value in zip(bars,counts.values):
            ax.text(
                bar.get_x()+bar.get_width()/2,
                bar.get_height(),
                str(value),
                ha="center",
                va="bottom",
                color="#1F3258",
                fontweight="bold"
            )

        st.pyplot(fig)

else:

    st.markdown("""
    <div class="hero">
        <h1>EDA Explorer</h1>
        <p>Upload a CSV dataset from the sidebar to begin your exploratory data analysis.</p>
    </div>
    """,unsafe_allow_html=True)

    st.info("Upload a CSV file using the sidebar to start exploring your dataset.")