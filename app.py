import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

campaign_df = pd.read_csv("campaign_performance.csv")
ad_df = pd.read_csv("ad_performance.csv")

st.set_page_config(page_title="Marketing Dashboard", layout="wide")

st.title("📊 Marketing Performance Dashboard")
st.write("Analyze the performance of campaigns and ads.")

selected_campaign = st.sidebar.selectbox("Select Campaign", ["All"] + list(campaign_df["Campaign Name"].unique()))
selected_ad = st.sidebar.selectbox("Select Ad", ["All"] + list(ad_df["Ad"].unique()))

st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Spend", f"${campaign_df['Spend'].sum():,.2f}")
col2.metric("Total Impressions", f"{campaign_df['Impressions'].sum():,}")
col3.metric("Total Clicks", f"{campaign_df['Clicks'].sum():,}")
col4.metric("Total Purchases", f"{campaign_df['Purchase'].sum():,}")

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

st.subheader("🏆 Best Performing Campaign")

campaign_df['CTR_norm'] = (campaign_df['CTR'] - campaign_df['CTR'].min()) / (campaign_df['CTR'].max() - campaign_df['CTR'].min())
campaign_df['CPC_norm'] = (campaign_df['CPC'].max() - campaign_df['CPC']) / (campaign_df['CPC'].max() - campaign_df['CPC'].min())

campaign_df['combined_score'] = campaign_df['CTR_norm'] + campaign_df['CPC_norm']

best_campaign = campaign_df.loc[campaign_df['combined_score'].idxmax()]

st.write(f"The best performing campaign is **{best_campaign['Campaign Name']}** with a combined score of **{best_campaign['combined_score']:.2f}**.")
st.write(f"CTR: **{best_campaign['CTR']:.2f}%**, CPC: **${best_campaign['CPC']:.2f}**")

st.write("This campaign performed the best because it had a high Click-Through Rate (CTR) and a low Cost Per Click (CPC), indicating that it was both effective and cost-efficient.")

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

st.subheader("🏆 Best Performing Ad")

ad_df['CTR_norm'] = (ad_df['CTR'] - ad_df['CTR'].min()) / (ad_df['CTR'].max() - ad_df['CTR'].min())
ad_df['CPC_norm'] = (ad_df['CPC'].max() - ad_df['CPC']) / (ad_df['CPC'].max() - ad_df['CPC'].min())

ad_df['combined_score'] = ad_df['CTR_norm'] + ad_df['CPC_norm']

best_ad = ad_df.loc[ad_df['combined_score'].idxmax()]

st.write(f"The best performing ad is **{best_ad['Ad']}** with a combined score of **{best_ad['combined_score']:.2f}**.")
st.write(f"CTR: **{best_ad['CTR']:.2f}%**, CPC: **${best_ad['CPC']:.2f}**")

st.write("This ad performed the best because it had a high Click-Through Rate (CTR) and a low Cost Per Click (CPC), indicating that it was both effective and cost-efficient.")

# Calculate total budget
total_budget = campaign_df['Spend'].sum()

# Set a minimum threshold for the combined score
min_threshold = 0.1

# Adjust the combined scores to ensure no campaign has a score of zero
campaign_df['adjusted_score'] = campaign_df['combined_score'].apply(lambda x: x if x > 0 else min_threshold)

# Calculate the proportion of the budget for each campaign based on adjusted scores
campaign_df['budget_proportion'] = campaign_df['adjusted_score'] / campaign_df['adjusted_score'].sum()

# Calculate the new budget allocation
campaign_df['new_budget'] = campaign_df['budget_proportion'] * total_budget

st.subheader("💰 Budget Redistribution")

# Display the new budget allocation
st.write("Based on the performance metrics (CTR and CPC), the budget for the campaigns would be redistributed as follows:")
st.dataframe(campaign_df[['Campaign Name', 'new_budget']])

# Explanation of the budget redistribution
st.write("The budget has been redistributed based on the combined score of CTR and CPC. Campaigns with higher combined scores receive a larger proportion of the budget, indicating better performance and cost-efficiency. A minimum threshold was applied to ensure a fair distribution.")


st.subheader("📜 Raw Data")
st.write("Campaign Performance Data (scroll right to see more columns)")
st.dataframe(campaign_df)

st.write("Ad Performance Data (scroll right to see more columns)")
st.dataframe(ad_df)