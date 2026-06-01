from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# Page configuration
st.set_page_config(
    page_title="NZ Kiwifruit Canopy Analysis",
    page_icon="🥝",
    layout="wide",
)


# Load data
@st.cache_data
def load_data():
    data_path = Path("data/kiwifruit_canopy_area_processed.csv")
    return pd.read_csv(data_path)


df = load_data()


# App title
st.title("🥝 New Zealand Kiwifruit Canopy Area Analysis")
st.subheader("2007–2024")

st.write(
    """
    This dashboard explores New Zealand kiwifruit canopy area trends using public data from Stats NZ.
    The goal is to understand how green, gold, and other kiwifruit varieties have changed over time.
    """
)


# Latest year metrics
latest_year = df.iloc[-1]

st.header("Latest Year Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Year", int(latest_year["year"]))
col2.metric("Total Canopy Area", f"{latest_year['total_canopy_area']:,.0f} ha")
col3.metric("Gold Kiwifruit Share", f"{latest_year['gold_share_pct']:.2f}%")
col4.metric("Green Kiwifruit Share", f"{latest_year['green_share_pct']:.2f}%")


# Dataset preview
st.header("Dataset Preview")
st.dataframe(df)


# Canopy area line chart
st.header("Canopy Area by Variety")

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df["year"], df["green_kiwifruit"], marker="o", label="Green Kiwifruit")
ax.plot(df["year"], df["gold_kiwifruit"], marker="o", label="Gold Kiwifruit")
ax.plot(df["year"], df["other_kiwifruit"], marker="o", label="Other Kiwifruit")

ax.set_title("New Zealand Kiwifruit Canopy Area by Variety, 2007–2024")
ax.set_xlabel("Year")
ax.set_ylabel("Canopy Area (hectares)")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)


# Percentage share chart
st.header("Percentage Share by Variety")

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df["year"], df["green_share_pct"], marker="o", label="Green Kiwifruit Share")
ax.plot(df["year"], df["gold_share_pct"], marker="o", label="Gold Kiwifruit Share")
ax.plot(df["year"], df["other_share_pct"], marker="o", label="Other Kiwifruit Share")

ax.set_title("New Zealand Kiwifruit Canopy Area Share by Variety, 2007–2024")
ax.set_xlabel("Year")
ax.set_ylabel("Share of Total Canopy Area (%)")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)


# Stacked bar chart
st.header("Total Canopy Area by Variety")

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(df["year"], df["green_kiwifruit"], label="Green Kiwifruit")
ax.bar(
    df["year"],
    df["gold_kiwifruit"],
    bottom=df["green_kiwifruit"],
    label="Gold Kiwifruit",
)
ax.bar(
    df["year"],
    df["other_kiwifruit"],
    bottom=df["green_kiwifruit"] + df["gold_kiwifruit"],
    label="Other Kiwifruit",
)

ax.set_title("Total New Zealand Kiwifruit Canopy Area by Variety, 2007–2024")
ax.set_xlabel("Year")
ax.set_ylabel("Canopy Area (hectares)")
ax.legend()
ax.grid(axis="y", alpha=0.3)

st.pyplot(fig)


# Insights
st.header("Key Insights")

st.write(
    """
    - Gold kiwifruit canopy area increased strongly between 2007 and 2024.
    - Green kiwifruit canopy area declined compared with 2007.
    - Gold kiwifruit became the largest variety by canopy area.
    - Other kiwifruit varieties remained much smaller but increased in recent years.
    """
)


# Data source
st.header("Data Source")

st.write(
    """
    Data source: Stats NZ Agricultural Production Statistics  
    Table: Kiwifruit canopy area hectares by variety, 2007–2024
    """
)