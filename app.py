import streamlit as st
import pandas as pd
import base64
from models.data_processor import load_data
from functions.visualizations import generate_popularity_trends, generate_audio_features, generate_genre_analysis, \
    generate_explicit_trends, generate_album_insights, generate_tempo_mood, generate_top_artists_songs, \
    generate_album_release_trends, generate_duration_analysis, generate_streaming_insights, \
    generate_feature_comparisons, generate_network_analysis

# Load data and display raw sample at the top
df = load_data()
if not df.empty:
    st.write("**Raw Data Sample:**", df.head())  # Display raw data sample
else:
    st.error("Failed to load raw data. Check the 'data/music_data.csv' file.")

# Sidebar
st.sidebar.title("Music Data Analysis")
# st.sidebar.markdown("[View Raw Data]('data/music_data.csv')", unsafe_allow_html=True)  # Replace with your Google Drive ID
analysis_option = st.sidebar.selectbox(
    "Choose Analysis",
    [
        "Popularity Trends Over Time",
        "Audio Features Analysis",
        "Genre & Artist Analysis",
        "Explicit Content Trends",
        "Album & Label Insights",
        "Tempo & Mood Analysis",
        "Top Artists and Songs",
        "Album Release Trends",
        "Track Duration Analysis",
        "Streaming and Engagement Insights",
        "Feature Comparisons Across Decades",
        "Network Analysis"
    ]
)

st.sidebar.subheader("Filters")
if not df.empty and 'Decade' in df.columns:
    decades = st.sidebar.multiselect("Select Decades", sorted(df['Decade'].unique()),
                                     default=sorted(df['Decade'].unique()))
    filtered_df = df[df['Decade'].isin(decades)] if decades else df
else:
    st.sidebar.warning(
        "No data loaded or 'Decade' column missing. Check the 'data' folder.")
    filtered_df = pd.DataFrame()

# Main content
# st.image("assets/spotify-logo.png", width=100)  # Spotify logo
st.title("Music Data Analysis Dashboard")
st.markdown("Explore trends and insights from a diverse music dataset.")

if analysis_option == "Popularity Trends Over Time":
    generate_popularity_trends(filtered_df)
elif analysis_option == "Audio Features Analysis":
    generate_audio_features(filtered_df)
elif analysis_option == "Genre & Artist Analysis":
    generate_genre_analysis(filtered_df)
elif analysis_option == "Explicit Content Trends":
    generate_explicit_trends(filtered_df)
elif analysis_option == "Album & Label Insights":
    generate_album_insights(filtered_df)
elif analysis_option == "Tempo & Mood Analysis":
    generate_tempo_mood(filtered_df)
elif analysis_option == "Top Artists and Songs":
    generate_top_artists_songs(filtered_df)
elif analysis_option == "Album Release Trends":
    generate_album_release_trends(filtered_df)
elif analysis_option == "Track Duration Analysis":
    generate_duration_analysis(filtered_df)
elif analysis_option == "Streaming and Engagement Insights":
    generate_streaming_insights(filtered_df)
elif analysis_option == "Feature Comparisons Across Decades":
    generate_feature_comparisons(filtered_df)
elif analysis_option == "Network Analysis":
    generate_network_analysis(filtered_df)

# Footer
# st.sidebar.markdown("Built with Streamlit by Grok 3 (xAI)")
