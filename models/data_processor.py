import pandas as pd
import streamlit as st

def load_data():
    try:
        df = pd.read_csv('data/music_data.csv', on_bad_lines='skip')
        st.write("**Raw Data Sample:**", df.head())
    except FileNotFoundError:
        st.error("Error: 'data/music_data.csv' not found. Please ensure the file exists.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading raw data: {e}")
        return pd.DataFrame()

    if df.empty:
        st.warning("Warning: Loaded DataFrame is empty. Check the CSV content.")
        return df

    if 'Album Release Date' not in df.columns:
        st.error("'Album Release Date' column missing from CSV")
        return df

    df['Year'] = pd.to_datetime(df['Album Release Date'], errors='coerce').dt.year
    df['Year'] = df['Year'].fillna(0).astype(int)
    df['Decade'] = (df['Year'] // 10 * 10).astype(int)

    df['Genres'] = df['Artist Genres'].fillna('Unknown').str.split(',').apply(lambda x: [g.strip() for g in x])
    df['Popularity'] = pd.to_numeric(df['Popularity'], errors='coerce').fillna(0)

    if 'Decade' not in df.columns:
        st.error("Failed to create 'Decade' column")
        return df
    st.write("**Processed Data Sample:**", df[['Track Name', 'Year', 'Decade', 'Popularity']].head())

    return df