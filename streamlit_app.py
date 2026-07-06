from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# Page configuration
st.set_page_config(
    page_title="NZ Kiwifruit Canopy Analysis",
    page_icon="🥝",
    layout="wide",
)

PROJECT_ROOT = Path(__file__).resolve().parent


# Load data
@st.cache_data
def load_data():
    data_path = PROJECT_ROOT / "data" / "kiwifruit_canopy_area_processed.csv"
    return pd.read_csv(data_path).sort_values("year")


df = load_data()

variety_area_columns = {
    "Green Kiwifruit": "green_kiwifruit",
    "Gold Kiwifruit": "gold_kiwifruit",
    "Other Kiwifruit": "other_kiwifruit",
}

variety_share_columns = {
    "Green Kiwifruit": "green_share_pct",
    "Gold Kiwifruit": "gold_share_pct",
    "Other Kiwifruit": "other_share_pct",
}

variety_options = list(variety_area_columns)

min_year = int(df["year"].min())
max_year = int(df["year"].max())


# Sidebar controls
with st.sidebar:
    st.header("Dashboard Controls")

    selected_year_range = st.slider(
        "Select year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
    )

    selected_varieties = st.multiselect(
        "Select kiwifruit varieties",
        options=variety_options,
        default=variety_options,
    )

    st.caption(
        "These controls update the table, charts, insights, and downloadable dataset."
    )


start_year, end_year = selected_year_range

filtered_df = df[
    df["year"].between(start_year, end_year)
].copy()

if not selected_varieties:
    st.warning("Select at least one kiwifruit variety from the sidebar to continue.")
    st.stop()


# Dashboard heading
st.title("🥝 New Zealand Kiwifruit Canopy Area Analysis")
st.subheader(f"{start_year}–{end_year}")

st.write(
    """
    Explore New Zealand kiwifruit canopy area trends using public Stats NZ data.
    Use the sidebar to focus on a period or varieties that interest you.
    """
)

st.divider()


# Latest-year metrics
latest_year = filtered_df.iloc[-1]

selected_latest_area = sum(
    latest_year[variety_area_columns[variety]]
    for variety in selected_varieties
)

leading_variety = max(
    selected_varieties,
    key=lambda variety: latest_year[variety_area_columns[variety]],
)

st.header("Latest Year Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Latest Year", int(latest_year["year"]))
col2.metric(
    "Total Industry Canopy Area",
    f"{latest_year['total_canopy_area']:,.0f} ha",
)
col3.metric(
    "Selected Varieties Area",
    f"{selected_latest_area:,.0f} ha",
)
col4.metric("Leading Selected Variety", leading_variety)

st.divider()


# Dataset preview and download
st.header("Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
)

filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered dataset as CSV",
    data=filtered_csv,
    file_name=f"kiwifruit_canopy_{start_year}_{end_year}.csv",
    mime="text/csv",
)

st.divider()


# Canopy area line chart
st.header("Canopy Area by Variety")

fig, ax = plt.subplots(figsize=(10, 6))

for variety in selected_varieties:
    ax.plot(
        filtered_df["year"],
        filtered_df[variety_area_columns[variety]],
        marker="o",
        label=variety,
    )

ax.set_title(f"New Zealand Kiwifruit Canopy Area by Variety, {start_year}–{end_year}")
ax.set_xlabel("Year")
ax.set_ylabel("Canopy Area (hectares)")
ax.set_xticks(filtered_df["year"])
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.divider()


# Percentage share chart
st.header("Percentage Share by Variety")

fig, ax = plt.subplots(figsize=(10, 6))

for variety in selected_varieties:
    ax.plot(
        filtered_df["year"],
        filtered_df[variety_share_columns[variety]],
        marker="o",
        label=f"{variety} Share",
    )

ax.set_title(f"New Zealand Kiwifruit Canopy Area Share by Variety, {start_year}–{end_year}")
ax.set_xlabel("Year")
ax.set_ylabel("Share of Total Canopy Area (%)")
ax.set_xticks(filtered_df["year"])
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.divider()


# Stacked bar chart
st.header("Total Canopy Area by Selected Variety")

fig, ax = plt.subplots(figsize=(10, 6))

bottom = pd.Series(0, index=filtered_df.index, dtype="float64")

for variety in selected_varieties:
    values = filtered_df[variety_area_columns[variety]]

    ax.bar(
        filtered_df["year"],
        values,
        bottom=bottom,
        label=variety,
    )

    bottom += values

ax.set_title(f"Total Canopy Area by Selected Variety, {start_year}–{end_year}")
ax.set_xlabel("Year")
ax.set_ylabel("Canopy Area (hectares)")
ax.set_xticks(filtered_df["year"])
ax.legend()
ax.grid(axis="y", alpha=0.3)

st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.divider()


# Dynamic insights
st.header("Key Insights")

first_year = filtered_df.iloc[0]

for variety in selected_varieties:
    first_value = first_year[variety_area_columns[variety]]
    latest_value = latest_year[variety_area_columns[variety]]
    change = latest_value - first_value

    if change > 0:
        direction = "increased"
    elif change < 0:
        direction = "decreased"
    else:
        direction = "remained unchanged"

    st.markdown(
        f"- **{variety}:** canopy area {direction} by "
        f"**{abs(change):,.0f} hectares** between {start_year} and {end_year}."
    )

st.markdown(
    f"- **Leading selected variety in {int(latest_year['year'])}:** "
    f"{leading_variety}."
)

st.info(
    "This dashboard shows national canopy-area trends. "
    "It does not represent individual orchard performance or farm-level yield."
)

st.divider()


# Data source
st.header("Data Source")

st.markdown(
    """
    **Source:** Stats NZ Agricultural Production Statistics

**Table:** Kiwifruit canopy area hectares by variety, 2007–2024
    """
)