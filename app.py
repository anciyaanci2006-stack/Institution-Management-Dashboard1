import streamlit as st
import pandas as pd
import plotly.express as px


# Page Configuration

st.set_page_config(
    page_title="SNGC College Dashboard",
    page_icon="🏫",
    layout="wide"
)


# Load Dataset

df = pd.read_excel("institution_management_dataset_500_rows.xlsx")


# Title

st.markdown(
    "<h1 style='text-align:center;color:#1f77b4;'>🏫 SNGC College - Institution Management Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown("---")


# Sidebar Filters

st.sidebar.header("🔍 Filter Students")

department = st.sidebar.selectbox(
    "Select Department",
    ["All"] + sorted(df["Department"].unique())
)

gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(df["Gender"].unique())
)

year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + sorted(df["Year"].unique())
)


# Apply Filters

filtered_df = df.copy()

if department != "All":
    filtered_df = filtered_df[
        filtered_df["Department"] == department
    ]

if gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"] == gender
    ]

if year != "All":
    filtered_df = filtered_df[
        filtered_df["Year"] == year
    ]


# Search Student

search = st.text_input("🔍 Search Student Name or Student ID")

if search:
    filtered_df = filtered_df[
        filtered_df["Student_Name"].str.contains(search, case=False, na=False)
        |
        filtered_df["Student_ID"].astype(str).str.contains(search)
    ]


# KPI Cards

k1, k2, k3, k4 = st.columns(4)

k1.metric("👨‍🎓 Total Students", len(filtered_df))
k2.metric(
    "📅 Avg Attendance",
    round(filtered_df["Attendance"].mean(),2)
)
k3.metric(
    "📚 Avg Marks",
    round(filtered_df["Marks"].mean(),2)
)
k4.metric(
    "💰 Pending Fees",
    len(filtered_df[
        filtered_df["Fees_Status"]=="Pending"
    ])
)

st.divider()

# =============================
# Create Charts
# =============================

# Department Chart
department_count = filtered_df["Department"].value_counts().reset_index()
department_count.columns = ["Department","Students"]

fig1 = px.bar(
    department_count,
    x="Department",
    y="Students",
    color="Department",
    title="Department-wise Student Count"
)

# Gender Chart
gender_count = filtered_df["Gender"].value_counts().reset_index()
gender_count.columns=["Gender","Students"]

fig2 = px.pie(
    gender_count,
    names="Gender",
    values="Students",
    title="Gender Distribution"
)

# Attendance
fig3 = px.histogram(
    filtered_df,
    x="Attendance",
    nbins=10,
    color="Department",
    title="Attendance Analysis"
)

# Marks
fig4 = px.histogram(

    filtered_df,
    x="Marks",
    nbins=10,
    color="Department",
    title="Marks Analysis"
)

# Fee Status
fee_count = filtered_df["Fees_Status"].value_counts().reset_index()
fee_count.columns=["Status","Students"]

fig5 = px.pie(
    fee_count,
    names="Status",
    values="Students",
    hole=0.4,
    title="Fee Status"
)

# Year Chart
year_count = filtered_df["Year"].value_counts().reset_index()
year_count.columns=["Year","Students"]

fig6 = px.bar(
    year_count,
    x="Year",
    y="Students",
    color="Year",
    title="Year-wise Student Count"
)

# =============================
# Dashboard Layout
# =============================

row1_col1,row1_col2=st.columns(2)

with row1_col1:
    st.plotly_chart(fig1,use_container_width=True)

with row1_col2:
    st.plotly_chart(fig2,use_container_width=True)

row2_col1,row2_col2=st.columns(2)

with row2_col1:
    st.plotly_chart(fig3,use_container_width=True)

with row2_col2:
    st.plotly_chart(fig4,use_container_width=True)

row3_col1,row3_col2=st.columns(2)

with row3_col1:
    st.plotly_chart(fig5,use_container_width=True)

with row3_col2:
    st.plotly_chart(fig6,use_container_width=True)

st.divider()

# =============================
# Student Table
# =============================

st.subheader("📋 Student Details")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =============================
# Download Button
# =============================

csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "student_data.csv",
    "text/csv"
)

st.success("✅ Dashboard Loaded Successfully!")
