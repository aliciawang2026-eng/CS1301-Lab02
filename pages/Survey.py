# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

from pathlib import Path
import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="GT Study Survey",
    page_icon="🐝",
)

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data.csv"

# PAGE TITLE AND USER DIRECTIONS
st.title("Georgia Tech Study Habits Survey 🐝")
st.write("Please fill out the form below to share your daily study habits at Georgia Tech.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    student_id = st.text_input("Enter your Name or GT Username:")
    study_hours = st.number_input(
        "How many hours do you study at Georgia Tech each night?",
        min_value=0.0,
        max_value=24.0,
        value=3.0,
        step=0.5,
    )
    workload_input = st.selectbox(
        "How would you rate your current workload?",
        ["Light", "Moderate", "Heavy", "Extreme"]
    )

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        if not student_id.strip():
            st.error("Please enter a name or GT Username before submitting.")
        else:
            new_data = pd.DataFrame(
                [{
                    "Student": student_id.strip(),
                    "Study_Hours": study_hours,
                    "Workload": workload_input,
                }]
            )

            file_exists = os.path.exists(csv_path) and os.path.getsize(csv_path) > 0
            new_data.to_csv(
                csv_path, mode="a", index=False, header=not file_exists
            )

            st.success("Your data has been submitted successfully! Go Jackets! 🐝")
            st.write(
                f"**Submitted:** Student: {student_id} | Study Hours: {study_hours} hrs/night | Workload: {workload_input}"
            )
        
# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
    current_data_df = pd.read_csv(csv_path)
    st.dataframe(current_data_df, use_container_width=True)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
