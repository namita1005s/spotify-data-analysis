import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

st.set_page_config(layout='wide')
st.title("Spotify Data Analysis App")
def load_data():
    df = pd.read_csv(r'C:\Users\Aditya PC\Desktop\spotify data analysis\data\SpotifyFeatures.csv')
    return df

df = load_data()


col1 ,col2 = st.columns(2)
with col1:
    st.dataframe(df)


with col2:
    numerical_columns = ['popularity', 'acousticness', 'danceability', 'duration_ms', 'energy',
                     'instrumentalness', 'key', 'liveness', 'loudness', 'speechiness',
                     'tempo', 'valence']

    st.sidebar.header("Distribution analysis")
    col = st.sidebar.selectbox("Select a column", numerical_columns)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.histplot(df[col], bins=20, kde=True, ax=ax)
    ax.set_title(f"{col}")
    st.pyplot(fig)

def genre_analysis(df):
    st.header("Genre Analysis")

    
    num_unique_genres = df['genre'].nunique()
    st.write(f"Number of Unique Genres: {num_unique_genres}")

   
    feature_choice = st.selectbox("Select a Feature for Analysis", ["popularity", "danceability", "energy"])
    
    
    genre_counts = df['genre'].value_counts()
    st.subheader("Distribution of Genres")
    fig_genre = px.bar(genre_counts, x=genre_counts.index, y=genre_counts.values, labels={"x": "Genre", "y": "Count"})
    st.plotly_chart(fig_genre)

    
    top_genre_count = st.slider("Number of Top Genres to Display", min_value=1, max_value=num_unique_genres, value=5)
    
    
    popular_genres = df.groupby('genre')[feature_choice].mean().sort_values(ascending=False).head(top_genre_count)
    st.subheader(f"Top {top_genre_count} Genres by {feature_choice.capitalize()}")
    st.write(popular_genres)

def artist_name_analysis(df):
    st.header("Artist Name Analysis")

   
    num_unique_artists = df['artist_name'].nunique()
    st.write(f"Number of Unique Artist Names: {num_unique_artists}")

    artist_name = st.text_input("Search for an Artist")
    
    if artist_name:
        
        filtered_df = df[df['artist_name'].str.contains(artist_name, case=False, na=False)]
        st.subheader(f"Tracks by {artist_name}")
        st.write(filtered_df[['track_name', 'popularity']])


def track_name_analysis(df):
    st.header("Track Name Analysis")

   
    num_unique_tracks = df['track_name'].nunique()
    st.write(f"Number of Unique Track Names: {num_unique_tracks}")

    
    track_name = st.text_input("Search for a Track")
    
    if track_name:
        
        filtered_df = df[df['track_name'].str.contains(track_name, case=False, na=False)]
        st.subheader(f"Details for Track: {track_name}")
        st.write(filtered_df)

def popularity_analysis(df):

    st.header("Popularity Analysis")
    st.subheader()

    
    st.subheader("Descriptive Statistics for Popularity")
    st.write(df['popularity'].describe())


    st.subheader("Popularity Distribution")
    fig_hist = px.histogram(df, x='popularity', nbins=num_bins, title="Popularity Distribution")
    st.plotly_chart(fig_hist)

    top_count = st.number_input("Number of Top Tracks to Display", min_value=1, max_value=len(df), value=10)
    bottom_count = st.number_input("Number of Bottom Tracks to Display", min_value=1, max_value=len(df), value=10)


    st.subheader(f"Top {top_count} Highly Popular Tracks")
    top_popular_tracks = df.nlargest(top_count, 'popularity')
    fig_top = go.Figure(data=[go.Table(header=dict(values=["Track Name", "Popularity"]),
                                       cells=dict(values=[top_popular_tracks['track_name'], top_popular_tracks['popularity']]))])
    st.plotly_chart(fig_top)

    st.subheader(f"Bottom {bottom_count} Less Popular Tracks")
    bottom_popular_tracks = df.nsmallest(bottom_count, 'popularity')
    fig_bottom = go.Figure(data=[go.Table(header=dict(values=["Track Name", "Popularity"]),
                                         cells=dict(values=[bottom_popular_tracks['track_name'], bottom_popular_tracks['popularity']]))])
    st.plotly_chart(fig_bottom)


def main():
    st.sidebar.title("Analysis Options")
    df = load_data()
    analysis_choice = st.sidebar.selectbox(
        "Select Analysis",
        ["Genre Analysis", "Artist Name Analysis", "Track Name Analysis", "Popularity Analysis"]
    )

    if analysis_choice == "Genre Analysis":
        genre_analysis(df)
    elif analysis_choice == "Artist Name Analysis":
        artist_name_analysis(df)
    elif analysis_choice == "Track Name Analysis":
        track_name_analysis(df)
    elif analysis_choice == "Popularity Analysis":
        popularity_analysis(df)

if __name__ == "__main__":
    main()
