# This creates the page for displaying data visualizations.

import streamlit as st
from pathlib import Path
import json
import os
import pandas as pd
import plotly.express as px


# PAGE CONFIGURATION
st.set_page_config(
    page_title="K-pop Visuals",
    page_icon="🎤",
)

# PAGE TITLE
st.title("Part 1: K-pop Album Sales Tracker 🎤")


# PART 1: GRAPHS FROM data.json

BASE_DIR = Path(__file__).resolve().parent.parent
json_path = BASE_DIR / "data.json"

with open(json_path,"r",encoding="utf-8") as infile:
    json_data=json.load(infile)

df_json=pd.DataFrame(json_data["album_sales"])

#static visualization
st.subheader("Static Chart: Total Album Sales by Group")
st.caption("A simple bar chart displaying total album sales (in thousands) per group.")

group_sales=df_json.groupby("group")["sales_thousands"].sum().reset_index()

st.bar_chart(
    data=group_sales,
    x="group",
    y="sales_thousands"
)

st.divider()

#dynamic visualization
st.subheader("Dynamic Advanced Chart: Monthly Album Sales Explorer")
st.caption("An interactive Plotly chart showing sales trends across months, filtered by minimum monthly sales")

if "min_sales" not in st.session_state:
    st.session_state["min_sales"]=200
    
st.session_state["min_sales"]=st.slider(
    "Select Minimum Monthly Sales (in Thousands):",
    min_value=200,
    max_value=500,
    step=10,
    value=st.session_state["min_sales"]
)

filtered_df=df_json[df_json["sales_thousands"]>=st.session_state["min_sales"]]

if not filtered_df.empty:
    fig=px.bar(
        filtered_df,
        x="month",
        y="sales_thousands",
        color="group",
        barmode="group",
        hover_data=["album","company"],
        title="Monthly K-pop Album Sales Comparison",
        labels={
            "month": "Month",
            "sales_thousands": "Sales (Thousands of Units)",
            "group": "Group Name",
            "album": "Album Title",
            "company": "Agency"
        }
    )
    st.plotly_chart(fig,use_container_width=True)
else:
    st.warning("No sales data available above the selected threshold.")
    

        
# PART 2: GRAPHS FROM data.csv
st.divider()
st.header("Part 2: GT Study Hours Analysis 🐝")

csv_path = BASE_DIR / "data.csv"

if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
    df_csv = pd.read_csv(csv_path)

    # 1. STATIC VISUALIZATION (Pie Chart - Workload Levels)
    st.subheader("Static Chart: Workload Level Distribution")
    st.caption(
        "Fixed distribution of participants across perceived GT workload"
        " intensity."
    )

    workload_counts = df_csv["Workload"].value_counts().reset_index()
    workload_counts.columns = ["Workload", "Count"]

    fig_static = px.pie(
        workload_counts,
        values="Count",
        names="Workload",
        title="Reported Workload Intensity at Georgia Tech",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    st.plotly_chart(fig_static, use_container_width=True)

    st.divider()

    # 2. DYNAMIC & ADVANCED VISUALIZATION (Scatter Plot with Session State)
    st.subheader("Dynamic Advanced Chart: Nightly Study Hours Explorer")
    st.caption(
        "Interactive scatter plot filtering study hours per GT student using"
        " Session State."
    )

    min_study_val = (
        float(df_csv["Study_Hours"].min()) if not df_csv.empty else 0.0
    )
    max_study_val = (
        float(df_csv["Study_Hours"].max()) if not df_csv.empty else 12.0
    )

    if "min_study_filter" not in st.session_state:
        st.session_state["min_study_filter"] = min_study_val

    st.session_state["min_study_filter"] = st.slider(
        "Filter minimum study hours per night to include:",
        min_value=min_study_val,
        max_value=max_study_val,
        value=st.session_state["min_study_filter"],
        step=0.5,
        key="csv_study_slider",
    )

    filtered_csv_df = df_csv[
        df_csv["Study_Hours"] >= st.session_state["min_study_filter"]
    ]

    if not filtered_csv_df.empty:
        fig_dynamic = px.scatter(
            filtered_csv_df,
            x="Student",
            y="Study_Hours",
            color="Workload",
            size="Study_Hours",
            title="Nightly Study Hours per GT Student",
            labels={
                "Student": "Student Name / ID",
                "Study_Hours": "Study Duration (Hours/Night)",
                "Workload": "Workload Rating",
            },
        )
        st.plotly_chart(fig_dynamic, use_container_width=True)

        # EXTRA CREDIT: Summary Statistics with st.metric()
        st.subheader("⚡ Live Summary Statistics (Extra Credit)")
        st.caption(
            "Real-time mean and median updates based on the slider filter."
        )

        overall_mean = df_csv["Study_Hours"].mean()
        overall_median = df_csv["Study_Hours"].median()

        current_mean = filtered_csv_df["Study_Hours"].mean()
        current_median = filtered_csv_df["Study_Hours"].median()

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Mean Study Hours (Filtered)",
                value=f"{current_mean:.2f} hrs",
                delta=f"{current_mean - overall_mean:+.2f} hrs vs overall",
            )
        with col2:
            st.metric(
                label="Median Study Hours (Filtered)",
                value=f"{current_median:.2f} hrs",
                delta=f"{current_median - overall_median:+.2f} hrs vs overall",
            )
    else:
        st.warning(
            "No student data matches the selected minimum study threshold."
        )
else:
    st.info(
        "No survey data found in `data.csv`. Please complete the Survey page to"
        " generate charts!"
    )
