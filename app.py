import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
campaign_df = pd.read_csv("campaign_performance.csv")
ad_df = pd.read_csv("ad_performance.csv")

# Streamlit Dashboard
st.set_page_config(page_title="Marketing Dashboard", layout="wide")

st.title("📊 Marketing Performance Dashboard")
st.write("Analyze the performance of campaigns and ads.")

# Sidebar Filters
selected_campaign = st.sidebar.selectbox("Select Campaign", ["All"] + list(campaign_df["Campaign Name"].unique()))
selected_ad = st.sidebar.selectbox("Select Ad", ["All"] + list(ad_df["Ad"].unique()))

# Metrics Display
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Spend", f"${campaign_df['Spend'].sum():,.2f}")
col2.metric("Total Impressions", f"{campaign_df['Impressions'].sum():,}")
col3.metric("Total Clicks", f"{campaign_df['Clicks'].sum():,}")
col4.metric("Total Purchases", f"{campaign_df['Purchase'].sum():,}")

# Campaign Performance
st.subheader("📊 Campaign Performance")

if selected_campaign != "All":
    filtered_df = campaign_df[campaign_df["Campaign Name"] == selected_campaign]
else:
    filtered_df = campaign_df

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="Campaign Name", y="CTR", data=filtered_df, ax=ax)
plt.xticks(rotation=90)
ax.set_title("Click-Through Rate (CTR) by Campaign")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="Campaign Name", y="CPC", data=filtered_df, ax=ax)
plt.xticks(rotation=90)
ax.set_title("Cost Per Click (CPC) by Campaign")
st.pyplot(fig)

# Ad Performance
st.subheader("🎯 Ad Performance")

if selected_ad != "All":
    filtered_ad_df = ad_df[ad_df["Ad"] == selected_ad]
else:
    filtered_ad_df = ad_df

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="Ad", y="CTR", data=filtered_ad_df, ax=ax)
plt.xticks(rotation=90)
ax.set_title("Click-Through Rate (CTR) by Ad")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="Ad", y="CPC", data=filtered_ad_df, ax=ax)
plt.xticks(rotation=90)
ax.set_title("Cost Per Click (CPC) by Ad")
st.pyplot(fig)

# Show Data
st.subheader("📜 Raw Data")
st.write("Campaign Performance Data")
st.dataframe(campaign_df)

st.write("Ad Performance Data")
st.dataframe(ad_df)
