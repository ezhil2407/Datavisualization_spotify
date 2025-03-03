import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Set page configuration
st.set_page_config(page_title="Music Popularity Trends", layout="wide")

# Title
st.title("Music Popularity Trends Over Time")

# Load the data from the 'data' folder
@st.cache_data
def load_data():
    # Define the path to the data folder
    data_path = os.path.join(os.getcwd(), 'data', 'music_data.csv')
    # Load the CSV file
    data = pd.read_csv(data_path)
    # Convert Album Release Date to datetime
    data['Album Release Date'] = pd.to_datetime(data['Album Release Date'], errors='coerce')
    # Extract year and decade
    data['Year'] = data['Album Release Date'].dt.year
    data['Decade'] = (data['Year'] // 10) * 10
    return data

# Load data
try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'music_data.csv' not found in the 'data' folder. Please ensure the file exists.")
    st.stop()

# Sidebar for filtering
st.sidebar.header("Filter Options")
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

# Filter data based on year range
filtered_df = df[
    (df['Year'] >= year_range[0]) & 
    (df['Year'] <= year_range[1])
]

# 1. Line Chart - Average Popularity by Decade
st.header("Average Popularity by Decade")
decade_avg = filtered_df.groupby('Decade')['Popularity'].mean().reset_index()

fig_line = px.line(
    decade_avg,
    x='Decade',
    y='Popularity',
    title='Average Song Popularity by Decade',
    labels={'Popularity': 'Average Popularity', 'Decade': 'Decade'},
    template='plotly_white'
)

fig_line.update_layout(
    xaxis=dict(tickmode='linear', dtick=10),
    yaxis=dict(range=[0, 100])
)

st.plotly_chart(fig_line, use_container_width=True)

# 2. Scatter Plot - Individual Song Popularity Over Time
st.header("Individual Song Popularity Over Time")
fig_scatter = px.scatter(
    filtered_df,
    x='Album Release Date',
    y='Popularity',
    hover_data=['Track Name', 'Artist Name(s)'],
    title='Song Popularity by Release Date',
    labels={'Album Release Date': 'Release Date', 'Popularity': 'Popularity'},
    template='plotly_white'
)

fig_scatter.update_traces(
    marker=dict(size=8, opacity=0.6),
    selector=dict(mode='markers')
)

fig_scatter.update_layout(
    yaxis=dict(range=[0, 100]),
    showlegend=False
)

st.plotly_chart(fig_scatter, use_container_width=True)

# Additional Insights
st.header("Key Insights")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Most Popular Decade")
    most_popular_decade = decade_avg.loc[decade_avg['Popularity'].idxmax()]
    st.write(f"Decade: {int(most_popular_decade['Decade'])}s")
    st.write(f"Average Popularity: {most_popular_decade['Popularity']:.1f}")

with col2:
    st.subheader("Most Popular Song")
    most_popular_song = filtered_df.loc[filtered_df['Popularity'].idxmax()]
    st.write(f"Track: {most_popular_song['Track Name']}")
    st.write(f"Artist: {most_popular_song['Artist Name(s)']}")
    st.write(f"Popularity: {most_popular_song['Popularity']}")
    st.write(f"Release Year: {int(most_popular_song['Year'])}")

# Notes
st.markdown("""
**Notes:**
- Popularity scores range from 0 to 100
""")