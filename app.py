import os
import pandas as pd
import streamlit as st
from models.data_processor import load_data
from functions.visualizations import (
    generate_popularity_trends, generate_audio_features, generate_genre_analysis,
    generate_explicit_trends, generate_album_insights, generate_tempo_mood,
    generate_top_artists_songs, generate_album_release_trends, generate_duration_analysis,
    generate_streaming_insights, generate_feature_comparisons, generate_network_analysis
)

# Load Data
df = load_data()

# Sidebar - Add Spotify Logo from URL at left top middle
# Using a reliable Spotify logo URL (fallback to green logo)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
                 width=150, caption="Spotify", use_column_width=False)

# Sidebar - Title & Filters
st.sidebar.title("Music Data Analysis")
analysis_option = st.sidebar.selectbox(
    "Choose Analysis",
    [
        "Popularity Trends Over Time", "Audio Features Analysis", "Genre & Artist Analysis",
        "Explicit Content Trends", "Album & Label Insights", "Tempo & Mood Analysis",
        "Top Artists and Songs", "Album Release Trends", "Track Duration Analysis",
        "Streaming and Engagement Insights", "Feature Comparisons Across Decades",
        "Network Analysis"
    ]
)

st.sidebar.subheader("Filters")
if not df.empty and 'Decade' in df.columns:
    decades = st.sidebar.multiselect("Select Decades", sorted(
        df['Decade'].unique()), default=sorted(df['Decade'].unique()))
    filtered_df = df[df['Decade'].isin(decades)] if decades else df
else:
    st.sidebar.warning(
        "No data loaded or 'Decade' column missing. Check the 'data' folder.")
    filtered_df = pd.DataFrame()

# Add View Raw Data link at the bottom of the sidebar
st.sidebar.markdown(
    "[View Raw Data Source](https://www.kaggle.com/datasets/joebeachcapital/top-10000-spotify-songs-1960-now)", unsafe_allow_html=True)

# Main Content
st.title("Music Data Analysis Dashboard")
st.markdown("Explore trends and insights from a diverse music dataset.")

# Call Analysis Functions Based on Selection with updated explanations
if analysis_option == "Popularity Trends Over Time":
    st.markdown("**Popularity Trends:** Tracks popularity changes over time.")
    generate_popularity_trends(filtered_df)
elif analysis_option == "Audio Features Analysis":
    st.markdown("**Audio Features:** Shows feature distributions.")
    generate_audio_features(filtered_df)
elif analysis_option == "Genre & Artist Analysis":
    st.markdown("**Genre & Artist:** Highlights top genres.")
    generate_genre_analysis(filtered_df)
elif analysis_option == "Explicit Content Trends":
    st.markdown("**Explicit Trends:** Compares explicit songs.")
    generate_explicit_trends(filtered_df)
elif analysis_option == "Album & Label Insights":
    st.markdown("**Album & Label:** Displays top labels.")
    generate_album_insights(filtered_df)
elif analysis_option == "Tempo & Mood Analysis":
    st.markdown("**Tempo & Mood:** Tracks tempo trends.")
    generate_tempo_mood(filtered_df)
elif analysis_option == "Top Artists and Songs":
    st.markdown("**Top Artists/Songs:** Lists top artists and songs.")
    generate_top_artists_songs(filtered_df)
elif analysis_option == "Album Release Trends":
    st.markdown("**Album Trends:** Shows release patterns.")
    generate_album_release_trends(filtered_df)
elif analysis_option == "Track Duration Analysis":
    st.markdown("**Duration Analysis:** Displays track durations.")
    generate_duration_analysis(filtered_df)
elif analysis_option == "Streaming and Engagement Insights":
    st.markdown("**Streaming Insights:** Explores engagement trends.")
    generate_streaming_insights(filtered_df)
elif analysis_option == "Feature Comparisons Across Decades":
    st.markdown("**Feature Comparisons:** Compares features across decades.")
    generate_feature_comparisons(filtered_df)
elif analysis_option == "Network Analysis":
    st.markdown("**Network Analysis:** Visualizes artist connections.")
    generate_network_analysis(filtered_df)
