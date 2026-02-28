import streamlit as st
import pandas as pd
import numpy as np

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Real Estate Analytics Dashboard", layout="wide")

st.title("🏠 Real Estate Analytics Dashboard")

# -------------------------------------------------
# CREATE DATA (20 Rows Only)
# -------------------------------------------------
np.random.seed(42)

dates = pd.date_range(start="2025-01-01", periods=20, freq="D")

property_type = np.random.choice(
    ["Condo", "Landed", "Apartment"], size=20
)

location = np.random.choice(
    ["Kuala Lumpur", "Selangor", "Penang"], size=20
)

price = np.random.randint(300000, 1500000, size=20)
size_sqft = np.random.randint(600, 3500, size=20)
bedrooms = np.random.randint(1, 6, size=20)

df = pd.DataFrame({
    "Listing Date": dates,
    "Property Type": property_type,
    "Location": location,
    "Price (RM)": price,
    "Size (sqft)": size_sqft,
    "Bedrooms": bedrooms
})

# Derived Metric
df["Price per sqft"] = df["Price (RM)"] / df["Size (sqft)"]

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
st.sidebar.header("Filter Data")

# your code here: create multiselect filters for Location, then filter the dataframe accordingly
selected_location =  st.sidebar.multiselect(
    "Select Location",
    options=sorted(df["Location"].unique()),
    default=sorted(df["Location"].unique())
)

# your code here: create multiselect filters for Property Type, then filter the dataframe accordingly
selected_property = st.sidebar.multiselect(
    "Select Property Type",
    options=sorted(df["Property Type"].unique()),
    default=sorted(df["Property Type"].unique())
)

# your code here: filter the dataframe based on the selected filters (use .copy() to avoid SettingWithCopyWarning)
filtered_df = df[
    (df["Location"].isin(selected_location)) &
    (df["Property Type"].isin(selected_property))
].copy()

# Guard (avoid empty selections causing NaNs / errors)
if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust the filters.")
    st.stop()

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.subheader("Key Market Metrics")

col1, col2, col3, col4 = st.columns(4)

# Fill in the missing code to calculate and display the average price, average size, average bedrooms, and average price per sqft in the respective columns
col1.metric("Average Price", f"RM {int(filtered_df['Price (RM)'].mean()):,}")
col2.metric("Average Size (sqft)", int(filtered_df["Size (sqft)"].mean()))
col3.metric("Average Bedrooms", round(filtered_df["Bedrooms"].mean(), 1))
col4.metric("Avg Price per sqft", f"RM {int(filtered_df['Price per sqft'].mean()):,}")

st.divider()

# -------------------------------------------------
# PRICE TREND (Line Chart)
# -------------------------------------------------
st.subheader("Price Trend Over Time")

line_df = filtered_df.set_index("Listing Date")[["Price (RM)"]].sort_index()

# your code here: create a line chart to show the price trend over time using st.line_chart

st.line_chart(line_df)
 

# -------------------------------------------------
# BAR CHART (Average Price by Property Type)
# -------------------------------------------------
st.subheader("Average Price by Property Type")

bar_data = filtered_df.groupby("Property Type", as_index=True)["Price (RM)"].mean().sort_values(ascending=False)

# your code here: create a bar chart to show the average price by property type using st.bar_chart
st.bar_chart(bar_data)

# -------------------------------------------------
# SCATTER CHART (Simple Streamlit Chart)
# -------------------------------------------------
st.subheader("Size vs Price (Color = Property Type)")
st.scatter_chart(filtered_df, x="Size (sqft)", y="Price (RM)")

# NOTE:
# Streamlit's built-in scatter chart does not support bubble sizes like Vega-Lite did.
# We'll keep a clean scatter with color grouping.
scatter_df = filtered_df[["Size (sqft)", "Price (RM)", "Property Type"]].copy()

# your code here: create a scatter chart to show the relationship between size and price, colored by property type using st.scatter_chart


# Optional: show the raw table for details/tooltip-like exploration
with st.expander("Show listing details"):
    st.dataframe(
        filtered_df.sort_values("Listing Date"),
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------
# HEATMAP (Simple Streamlit Alternative)
# -------------------------------------------------
st.subheader("Heatmap: Avg Price by Location & Property Type")

# Streamlit doesn't have a native heatmap chart (without Altair/Plotly).
# A simple alternative is a pivot table + color gradient styling.
heatmap_pivot = (
    filtered_df
    .pivot_table(index="Location", columns="Property Type", values="Price (RM)", aggfunc="mean")
    .round(0)
)

st.dataframe(
    heatmap_pivot.style.format("RM {:,.0f}").background_gradient(axis=None),
    use_container_width=True
)

# -------------------------------------------------
# HISTOGRAM (Simple Streamlit Alternative)
# -------------------------------------------------
st.subheader("Price Distribution")

# Your code here: Create bins and counts, then plot with st.bar_chart 
counts, edges = np.histogram(filtered_df["Price (RM)"], bins=8)

hist_df = pd.DataFrame({
    "Price Bin": [f"RM {int(edges[i]):,} - {int(edges[i+1]):,}" for i in range(len(edges) - 1)],
    "Count": counts
}).set_index("Price Bin")

st.bar_chart(hist_df)

# your code here: create a bar chart to show the price distribution 

st.divider()
st.caption("Demo dataset: 20 simulated property listings")