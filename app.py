import streamlit as st
import pandas as pd
import altair as alt

# --- Page Configuration ---
# Set the title and layout for your app
st.set_page_config(
    page_title="UK House Price EDA",
    layout="wide"
)

# --- Data Loading ---
# We use @st.cache_data to load the data only once,
# making the app faster.
@st.cache_data
def load_data(csv_path):
    # Load the dataframe
    df = pd.read_csv(csv_path)
    
    # Clean the data (same as in your notebook)
    df['Date'] = pd.to_datetime(df['Date'])
    # Drop the column with too many missing values
    df_cleaned = df.drop(columns=['Average_Price_SA'])
    return df_cleaned

# Load the data using the function
# Assumes the CSV is in the same folder as app.py
try:
    df_cleaned = load_data("Average-prices-2025-06.csv")
except FileNotFoundError:
    st.error("Error: 'Average-prices-2025-06.csv' not found. Make sure it's in the same folder as app.py.")
    st.stop()


# --- Start Building the App ---

# 1. Title
st.title("Exploratory Data Analysis: UK House Prices 🏠")
st.write("This interactive app analyzes average house prices from 1968 to 2025.")

# --- Section 1: Data Overview ---
st.header("1. Data Overview")

# Add a checkbox to toggle the view of the raw data
if st.checkbox("Show raw data"):
    st.write(f"Data contains {df_cleaned.shape[0]} rows and {df_cleaned.shape[1]} columns.")
    st.dataframe(df_cleaned)

# Display the summary statistics
st.subheader("Summary Statistics")
st.write("Descriptive statistics for the main numerical columns:")
st.write(df_cleaned.describe())


# --- Section 2: Time Series Analysis ---
st.header("2. Price Trends Over Time")

# Get a list of all unique regions for the dropdown menu
all_regions = df_cleaned['Region_Name'].unique()

# Create a select box (dropdown) for the user to choose a region
selected_region = st.selectbox(
    "Select a Region to Analyze:",
    options=all_regions,
    index=list(all_regions).index("United Kingdom")  # Set 'United Kingdom' as the default
)

# Filter the data based on the user's selection
df_region = df_cleaned[df_cleaned['Region_Name'] == selected_region]

# Create the Altair line chart
st.subheader(f"Average Price in {selected_region}")

time_series_chart = alt.Chart(df_region).mark_line().encode(
    x=alt.X('Date', title='Date'),
    y=alt.Y('Average_Price', title='Average Price (GBP)'),
    tooltip=[
        alt.Tooltip('Date', format='%Y-%m-%d'),
        alt.Tooltip('Average_Price', format=',.0f')
    ]
).properties(
    title=f"Average House Price in {selected_region} Over Time"
).interactive() # .interactive() makes the chart zoomable and pannable

# Display the chart in the Streamlit app
st.altair_chart(time_series_chart, use_container_width=True)


# --- Section 3: Regional Comparison (Latest Data) ---
st.header("3. Regional Price Comparison")

# Find the most recent date in the dataset
latest_date = df_cleaned['Date'].max()

st.subheader(f"Top 10 Most Expensive Regions on {latest_date.date()}")

# Filter the data for only that latest date
df_latest = df_cleaned[df_cleaned['Date'] == latest_date]

# Sort by price and get the top 10
df_top_10 = df_latest.sort_values(by='Average_Price', ascending=False).head(10)

# Create the Altair bar chart
bar_chart = alt.Chart(df_top_10).mark_bar().encode(
    # Sort the y-axis by the x-axis value in descending order
    y=alt.Y('Region_Name', sort='-x', title='Region Name'),
    x=alt.X('Average_Price', title=f'Average Price (GBP)'),
    tooltip=[
        alt.Tooltip('Region_Name'),
        alt.Tooltip('Average_Price', format=',.0f')
    ]
).properties(
    title=f"Top 10 Regions by Average Price ({latest_date.date()})"
)

# Display the bar chart
st.altair_chart(bar_chart, use_container_width=True)
