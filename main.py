import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_csv("growth_operations.csv")

def clean_currency(value):
    return float(value.replace("$", "").replace(",", ""))

numeric_cols = ["Spend", "CPM", "Impressions", "Clicks"]
for col in numeric_cols:
    df[col] = df[col].apply(clean_currency)

campaign_performance = df.groupby("Campaign Name").agg({
    "Spend": "sum",
    "Impressions": "sum",
    "Clicks": "sum",
    "Add to Cart": "sum",
    "Add Payment Info": "sum",
    "Purchase": "sum"
}).reset_index()


campaign_performance["CTR"] = campaign_performance["Clicks"] / campaign_performance["Impressions"]
campaign_performance["CR"] = campaign_performance["Purchase"] / campaign_performance["Clicks"]
campaign_performance["CPC"] = campaign_performance["Spend"] / campaign_performance["Clicks"]
campaign_performance["CPM"] = (campaign_performance["Spend"] / campaign_performance["Impressions"]) * 1000

campaign_performance.to_csv("campaign_performance.csv", index=False)

ad_performance = df.groupby("Ad").agg({
    "Spend": "sum",
    "Impressions": "sum",
    "Clicks": "sum",
    "Add to Cart": "sum",
    "Add Payment Info": "sum",
    "Purchase": "sum"
}).reset_index()

ad_performance["CTR"] = ad_performance["Clicks"] / ad_performance["Impressions"]
ad_performance["CR"] = ad_performance["Purchase"] / ad_performance["Clicks"]
ad_performance["CPC"] = ad_performance["Spend"] / ad_performance["Clicks"]
ad_performance["CPM"] = (ad_performance["Spend"] / ad_performance["Impressions"]) * 1000

ad_performance.to_csv("ad_performance.csv", index=False)
