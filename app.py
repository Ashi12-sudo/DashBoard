import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ----------------------
# Mock Data Generation
# ----------------------
np.random.seed(42)

incident_types = ["Network", "Application", "Database", "Security", "Infrastructure"]
priorities = ["P1", "P2", "P3", "P4"]
status_list = ["Open", "In Progress", "Resolved", "Escalated"]
teams = ["L1 Support", "L2 Support", "DevOps", "Security Ops"]

n = 200

data = pd.DataFrame({
    "Incident_ID": range(1000, 1000+n),
    "Type": np.random.choice(incident_types, n),
    "Priority": np.random.choice(priorities, n, p=[0.1, 0.2, 0.4, 0.3]),
    "Status": np.random.choice(status_list, n),
    "Assigned_Team": np.random.choice(teams, n),
    "Created_Time": [datetime.now() - timedelta(hours=np.random.randint(1, 240)) for _ in range(n)],
    "Resolution_Time_Hrs": np.random.randint(1, 72, n)
})

# ----------------------
# AI Recommendation Mock
# ----------------------
def ai_recommendation(row):
    if row["Priority"] == "P1":
        return "Immediate escalation recommended"
    if row["Type"] == "Security":
        return "Run security playbook"
    if row["Type"] == "Database":
        return "Check DB connections and logs"
    return "Follow standard troubleshooting guide"


data["AI_Recommendation"] = data.apply(ai_recommendation, axis=1)

# ----------------------
# Sidebar Filters
# ----------------------
st.sidebar.title("Filters")

selected_priority = st.sidebar.multiselect("Priority", priorities, default=priorities)
selected_team = st.sidebar.multiselect("Assigned Team", teams, default=teams)
selected_status = st.sidebar.multiselect("Status", status_list, default=status_list)

filtered_df = data[
    (data["Priority"].isin(selected_priority)) &
    (data["Assigned_Team"].isin(selected_team)) &
    (data["Status"].isin(selected_status))
]

# ----------------------
# Header
# ----------------------
st.title("IT Services Incident Response Assistant")
st.caption("AI-driven Incident Detection, Triage and Resolution Support")

# ----------------------
# KPI Section
# ----------------------
st.subheader("Operational KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Incidents", len(filtered_df))
col2.metric("Open Incidents", len(filtered_df[filtered_df["Status"] == "Open"]))
col3.metric("P1 Incidents", len(filtered_df[filtered_df["Priority"] == "P1"]))
col4.metric("Avg Resolution Time (hrs)", round(filtered_df["Resolution_Time_Hrs"].mean(), 2))

# ----------------------
# Incident Trend
# ----------------------
st.subheader("Incident Trend (Last 10 Days)")

trend = filtered_df.copy()
trend["Date"] = trend["Created_Time"].dt.date
trend_data = trend.groupby("Date").size()
st.line_chart(trend_data)

# ----------------------
# Incident Distribution
# ----------------------
st.subheader("Incident Distribution by Type")
st.bar_chart(filtered_df["Type"].value_counts())

st.subheader("Incident Distribution by Priority")
st.bar_chart(filtered_df["Priority"].value_counts())

# ----------------------
# AI Support Guidance Panel
# ----------------------
st.subheader("AI Support Guidance")

selected_incident = st.selectbox("Select Incident ID", filtered_df["Incident_ID"])
incident_details = filtered_df[filtered_df["Incident_ID"] == selected_incident]

st.write("### Incident Details")
st.dataframe(incident_details)

st.write("### AI Recommended Action")
st.success(incident_details["AI_Recommendation"].values[0])

# ----------------------
# Leadership Analytics
# ----------------------
st.subheader("Support Leadership Insights")

team_perf = filtered_df.groupby("Assigned_Team")["Resolution_Time_Hrs"].mean().sort_values()
st.write("Average Resolution Time by Team")
st.bar_chart(team_perf)

priority_perf = filtered_df.groupby("Priority")["Resolution_Time_Hrs"].mean().sort_values()
st.write("Resolution Time by Priority")
st.bar_chart(priority_perf)

# ----------------------
# Footer
# ----------------------
st.caption("Designed for IT Service Management | AI Assisted Incident Response")
