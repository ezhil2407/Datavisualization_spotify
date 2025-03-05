import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go
from itertools import combinations

def generate_popularity_trends(df):
    st.header("Popularity Trends Over Time")
    tab1, tab2 = st.tabs(["Average Popularity", "Individual Songs"])
    with tab1:
        st.markdown("**Average Popularity by Decade:** Tracks popularity changes over time.")
        if 'Decade' in df.columns:
            avg_pop_by_decade = df.groupby('Decade')['Popularity'].mean().reset_index()
            fig1 = px.line(avg_pop_by_decade, x='Decade', y='Popularity', title='Average Popularity by Decade', color_discrete_sequence=['blue'])
            fig1.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig1)
        else:
            st.error("Cannot plot: 'Decade' column missing.")
    with tab2:
        st.markdown("**Song Popularity Over Time:** Highlights individual trends.")
        if 'Year' in df.columns:
            fig2 = px.scatter(df, x='Year', y='Popularity', title='Song Popularity Over Time', hover_data=['Track Name', 'Artist Name(s)'], color_discrete_sequence=['red'])
            fig2.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig2)
        else:
            st.error("Cannot plot: 'Year' column missing.")

def generate_audio_features(df):
    st.header("Audio Features Analysis")
    feature = st.selectbox("Select Feature", ['Danceability', 'Energy', 'Tempo', 'Loudness'])
    tab1, tab2, tab3 = st.tabs(["Distribution", "By Decade", "Correlations"])
    with tab1:
        st.markdown(f"**Distribution of {feature}:** Shows feature variations.")
        fig3 = px.histogram(df, x=feature, title=f'Distribution of {feature}', color_discrete_sequence=['green'])
        fig3.update_layout(template='plotly_white', width=800, height=400)
        st.plotly_chart(fig3)
    with tab2:
        st.markdown(f"**{feature} by Decade:** Compares across decades.")
        if 'Decade' in df.columns:
            fig4 = px.box(df, x='Decade', y=feature, title=f'{feature} Distribution by Decade', color_discrete_sequence=['green'])
            fig4.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig4)
        else:
            st.error("Cannot plot: 'Decade' column missing.")
    with tab3:
        st.markdown("**Feature Correlations:** Explores relationships.")
        fig, ax = plt.subplots()
        sns.pairplot(df[['Energy', 'Danceability', 'Valence', 'Tempo']])
        st.pyplot(fig)

def generate_genre_analysis(df):
    st.header("Genre & Artist Analysis")
    tab1, tab2, tab3 = st.tabs(["Top Genres", "Genre Distribution", "Artist Popularity"])
    with tab1:
        st.markdown("**Top Genres by Decade:** Highlights frequent genres.")
        if 'Decade' in df.columns:
            genre_decade = df.explode('Genres').groupby(['Decade', 'Genres']).size().reset_index(name='Count')
            top_genres = genre_decade.groupby('Decade').apply(lambda x: x.nlargest(5, 'Count')).reset_index(drop=True)
            fig5 = px.bar(top_genres, x='Decade', y='Count', color='Genres', title='Top Genres by Decade', color_discrete_sequence=px.colors.qualitative.Set1)
            fig5.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig5)
        else:
            st.error("Cannot plot: 'Decade' column missing.")
    with tab2:
        st.markdown("**Genre Distribution:** Breaks down genres.")
        genre_counts = df.explode('Genres')['Genres'].value_counts().reset_index()
        fig6 = px.pie(genre_counts, values='count', names='Genres', title='Genre Distribution', color_discrete_sequence=px.colors.qualitative.Set2)
        fig6.update_layout(width=800, height=400)
        st.plotly_chart(fig6)
    with tab3:
        st.markdown("**Artist Popularity Heatmap:** Visualizes popularity.")
        if 'Artist Name(s)' in df.columns:
            artist_pop = df.groupby('Artist Name(s)')['Popularity'].mean().reset_index()
            fig7 = px.imshow(pd.pivot_table(df, values='Popularity', index='Artist Name(s)', aggfunc='mean').fillna(0), title='Artist Popularity Heatmap', color_continuous_scale='Reds')
            fig7.update_layout(width=800, height=400)
            st.plotly_chart(fig7)
        else:
            st.error("Cannot plot: 'Artist Name(s)' column missing.")

def generate_explicit_trends(df):
    st.header("Explicit Content Trends")
    st.markdown("**Explicit vs Non-Explicit Songs:** Compares content.")
    if 'Decade' in df.columns and 'Explicit' in df.columns:
        explicit_by_decade = df.groupby(['Decade', 'Explicit']).size().unstack().fillna(0)
        fig8 = px.bar(explicit_by_decade, barmode='stack', title='Explicit vs Non-Explicit Songs by Decade', color_discrete_sequence=['green', 'purple'])
        fig8.update_layout(template='plotly_white', width=800, height=400)
        st.plotly_chart(fig8)
    else:
        st.error("Cannot plot: 'Decade' or 'Explicit' column missing.")

def generate_album_insights(df):
    st.header("Album & Label Insights")
    tab1, tab2 = st.tabs(["Top Labels", "Album Popularity"])
    with tab1:
        st.markdown("**Top Record Labels:** Identifies top labels.")
        if 'Label' in df.columns:
            top_labels = df['Label'].value_counts().nlargest(10).reset_index()
            fig9 = px.bar(top_labels, x='Label', y='count', title='Top Record Labels by Song Count', color_discrete_sequence=['blue'])
            fig9.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig9)
        else:
            st.error("Cannot plot: 'Label' column missing.")
    with tab2:
        st.markdown("**Album Popularity:** Shows album trends.")
        if 'Album Name' in df.columns and 'Popularity' in df.columns:
            album_pop = df.groupby('Album Name')['Popularity'].agg(['mean', 'count']).reset_index()
            fig10 = px.scatter(album_pop, x='count', y='mean', size='mean', hover_data=['Album Name'], title='Albums: Song Count vs Average Popularity', color_discrete_sequence=['red'])
            fig10.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig10)
        else:
            st.error("Cannot plot: 'Album Name' or 'Popularity' column missing.")

def generate_tempo_mood(df):
    st.header("Tempo & Mood Analysis")
    tab1, tab2 = st.tabs(["Tempo Trends", "Mood Scatter"])
    with tab1:
        st.markdown("**Tempo Trends:** Tracks tempo changes.")
        if 'Year' in df.columns and 'Tempo' in df.columns:
            tempo_by_year = df.groupby('Year')['Tempo'].mean().reset_index()
            fig11 = px.line(tempo_by_year, x='Year', y='Tempo', title='Average Tempo Over Time', color_discrete_sequence=['orange'])
            fig11.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig11)
        else:
            st.error("Cannot plot: 'Year' or 'Tempo' column missing.")
    with tab2:
        st.markdown("**Valence vs Energy:** Groups mood patterns.")
        if 'Valence' in df.columns and 'Energy' in df.columns:
            fig12 = px.scatter(df, x='Valence', y='Energy', title='Valence vs Energy', hover_data=['Track Name'], color_discrete_sequence=['purple'])
            fig12.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig12)
        else:
            st.error("Cannot plot: 'Valence' or 'Energy' column missing.")

def generate_top_artists_songs(df):
    st.header("Top Artists and Songs")
    tab1, tab2 = st.tabs(["Top Artists", "Top Songs"])
    with tab1:
        st.markdown("**Most Featured Artists:** Shows top artists.")
        if 'Artist Name(s)' in df.columns:
            top_artists = df['Artist Name(s)'].value_counts().nlargest(10).reset_index()
            fig13 = px.bar(top_artists, x='Artist Name(s)', y='count', title='Most Featured Artists', color_discrete_sequence=['green'])
            fig13.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig13)
        else:
            st.error("Cannot plot: 'Artist Name(s)' column missing.")
    with tab2:
        st.markdown("**Top 10 Songs:** Lists top songs.")
        if 'Track Name' in df.columns and 'Popularity' in df.columns:
            top_songs = df.nlargest(10, 'Popularity')[['Track Name', 'Popularity']]
            fig14 = px.bar(top_songs, y='Track Name', x='Popularity', orientation='h', title='Top 10 Songs by Popularity', color_discrete_sequence=['blue'])
            fig14.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig14)
        else:
            st.error("Cannot plot: 'Track Name' or 'Popularity' column missing.")

def generate_album_release_trends(df):
    st.header("Album Release Trends")
    tab1, tab2 = st.tabs(["Albums per Year", "Artist-Year Heatmap"])
    with tab1:
        st.markdown("**Albums per Year:** Tracks release patterns.")
        if 'Year' in df.columns:
            albums_per_year = df['Year'].value_counts().sort_index().reset_index()
            fig15 = px.line(albums_per_year, x='Year', y='count', title='Number of Albums Released per Year', color_discrete_sequence=['purple'])
            fig15.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig15)
        else:
            st.error("Cannot plot: 'Year' column missing.")
    with tab2:
        st.markdown("**Songs by Artists and Years:** Visualizes trends.")
        if 'Artist Name(s)' in df.columns and 'Year' in df.columns:
            artist_year = df.groupby(['Artist Name(s)', 'Year']).size().unstack().fillna(0)
            fig16 = px.imshow(artist_year, title='Songs Released by Artists Across Years', color_continuous_scale='Viridis')
            fig16.update_layout(width=800, height=400)
            st.plotly_chart(fig16)
        else:
            st.error("Cannot plot: 'Artist Name(s)' or 'Year' column missing.")

def generate_duration_analysis(df):
    st.header("Track Duration Analysis")
    tab1, tab2 = st.tabs(["Distribution", "By Decade"])
    with tab1:
        st.markdown("**Track Duration Distribution:** Shows duration lengths.")
        if 'Track Duration (ms)' in df.columns:
            fig17 = px.histogram(df, x='Track Duration (ms)', title='Distribution of Track Durations', color_discrete_sequence=['orange'])
            fig17.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig17)
        else:
            st.error("Cannot plot: 'Track Duration (ms)' column missing.")
    with tab2:
        st.markdown("**Duration by Decade:** Compares durations.")
        if 'Decade' in df.columns and 'Track Duration (ms)' in df.columns:
            fig18 = px.box(df, x='Decade', y='Track Duration (ms)', title='Track Duration by Decade', color_discrete_sequence=['green'])
            fig18.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig18)
        else:
            st.error("Cannot plot: 'Decade' or 'Track Duration (ms)' column missing.")

def generate_streaming_insights(df):
    st.header("Streaming and Engagement Insights")
    tab1, tab2 = st.tabs(["Popularity vs Duration", "Time Signature"])
    with tab1:
        st.markdown("**Popularity vs Duration:** Explores engagement trends.")
        if 'Track Duration (ms)' in df.columns and 'Popularity' in df.columns:
            fig19 = px.scatter(df, x='Track Duration (ms)', y='Popularity', title='Popularity vs Track Duration', color_discrete_sequence=['blue'])
            fig19.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig19)
        else:
            st.error("Cannot plot: 'Track Duration (ms)' or 'Popularity' column missing.")
    with tab2:
        st.markdown("**Popularity by Time Signature:** Compares popularity.")
        if 'Time Signature' in df.columns and 'Popularity' in df.columns:
            pop_by_time = df.groupby('Time Signature')['Popularity'].mean().reset_index()
            fig20 = px.bar(pop_by_time, x='Time Signature', y='Popularity', title='Average Popularity by Time Signature', color_discrete_sequence=['purple'])
            fig20.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig20)
        else:
            st.error("Cannot plot: 'Time Signature' or 'Popularity' column missing.")

def generate_feature_comparisons(df):
    st.header("Feature Comparisons Across Decades")
    tab1, tab2 = st.tabs(["Feature Comparison", "Loudness Trends"])
    with tab1:
        st.markdown("**Feature Comparison:** Compares features across decades.")
        if 'Decade' in df.columns:
            features_by_decade = df.groupby('Decade')[['Danceability', 'Energy', 'Valence']].mean().reset_index()
            fig21 = px.bar(features_by_decade.melt(id_vars='Decade'), x='Decade', y='value', color='variable',
                           barmode='group', title='Feature Comparison by Decade', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig21.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig21)
        else:
            st.error("Cannot plot: 'Decade' column missing.")
    with tab2:
        st.markdown("**Loudness Over Time:** Tracks loudness trends.")
        if 'Year' in df.columns and 'Loudness' in df.columns:
            loudness_by_year = df.groupby('Year')['Loudness'].mean().reset_index()
            fig22 = px.line(loudness_by_year, x='Year', y='Loudness', title='Average Loudness Over Time', color_discrete_sequence=['green'])
            fig22.update_layout(template='plotly_white', width=800, height=400)
            st.plotly_chart(fig22)
        else:
            st.error("Cannot plot: 'Year' or 'Loudness' column missing.")

def generate_network_analysis(df):
    st.header("Network Analysis")
    tab1, tab2 = st.tabs(["Artist Collaborations", "Genre Crossover"])
    with tab1:
        st.markdown("**Artist Collaborations:** Visualizes artist connections.")
        if 'Artist Name(s)' in df.columns:
            valid_artists = df['Artist Name(s)'].dropna().astype(str)
            G = nx.Graph()
            for artists in valid_artists:
                artists_list = [a.strip() for a in artists.split(',') if a.strip()]
                if len(artists_list) > 1:
                    for a1, a2 in combinations(artists_list, 2):
                        G.add_edge(a1, a2)
            if G.number_of_nodes() > 0:
                pos = nx.spring_layout(G)
                edge_x = []
                edge_y = []
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])

                edge_trace = go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=0.5, color='#888'),
                    hoverinfo='none',
                    mode='lines')

                node_x = [pos[node][0] for node in G.nodes()]
                node_y = [pos[node][1] for node in G.nodes()]
                node_trace = go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers+text',
                    hoverinfo='text',
                    marker=dict(size=10, color='red'),
                    text=list(G.nodes()),
                    textposition="top center")

                fig = go.Figure(data=[edge_trace, node_trace],
                                layout=go.Layout(
                    title='Artist Collaborations',
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=40),
                    width=800, height=600))
                st.plotly_chart(fig)
            else:
                st.warning("No artist collaborations to display.")
        else:
            st.error("Cannot plot: 'Artist Name(s)' column missing.")
    with tab2:
        st.markdown("**Genre Crossover:** Placeholder for future visualization.")
        st.write("To implement, install `holoviews` and use the following code:")
        st.code("""
        import holoviews as hv
        hv.extension('bokeh')
        genre_pairs = df.explode('Genres')[['Genres']].merge(df.explode('Genres')[['Genres']], how='cross')
        chord_data = genre_pairs.groupby(['Genres_x', 'Genres_y']).size().reset_index(name='value')
        chord = hv.Chord(chord_data).opts(title="Genre Crossover")
        st.write(hv.render(chord, backend='bokeh'))
        """)