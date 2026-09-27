import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="6G Manufacturing Dashboard", layout="wide")

st.title("🏭 Impact of 6G Network Performance on Manufacturing Efficiency")
st.markdown("### Unified Mentor Internship Project - Thales Group Analysis")

@st.cache_data
def load_data():
    return pd.read_csv('/content/Thales_Group_Manufacturing_Processed.csv')

df = load_data()

st.sidebar.header("Dashboard Filters")

# Using selectbox instead of multiselect to avoid localtunnel JS loading errors
status_options = ['All'] + list(df['Efficiency_Status'].unique())
selected_status = st.sidebar.selectbox("Select Efficiency Status", options=status_options)

min_lat = float(df['Network_Latency_ms'].min())
max_lat = float(df['Network_Latency_ms'].max())
slider_max_lat = st.sidebar.slider("Max Latency (ms)", min_lat, max_lat, max_lat)

# Filter dataframe
if selected_status == 'All':
    filtered_df = df[df['Network_Latency_ms'] <= slider_max_lat]
else:
    filtered_df = df[(df['Efficiency_Status'] == selected_status) & (df['Network_Latency_ms'] <= slider_max_lat)]

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", len(filtered_df))
col2.metric("Avg Latency (ms)", round(filtered_df['Network_Latency_ms'].mean(), 2) if len(filtered_df) > 0 else 0)
col3.metric("Avg Stability Index", round(filtered_df['Network_Stability_Index'].mean(), 2) if len(filtered_df) > 0 else 0)
col4.metric("Avg Defect Rate (%)", round(filtered_df['Quality_Control_Defect_Rate_%'].mean(), 2) if len(filtered_df) > 0 else 0)

st.markdown("---")

# Visualizations
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Latency vs Production Speed")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=filtered_df, x='Network_Latency_ms', y='Production_Speed_units_per_hr', hue='Efficiency_Status', palette='viridis', ax=ax)
    st.pyplot(fig)

with col_b:
    st.subheader("Packet Loss vs Defect Rate")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=filtered_df, x='Packet_Loss_%', y='Quality_Control_Defect_Rate_%', hue='Efficiency_Status', palette='magma', ax=ax)
    st.pyplot(fig)

st.success("Dashboard loaded successfully without errors!")
