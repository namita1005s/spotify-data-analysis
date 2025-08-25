import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go

# ================= Page Setup =================
st.set_page_config(page_title="Spotify Data Analysis", layout="wide")
st.title("🎵 Spotify Data Analysis App")

# ================= Load Dataset =================
@st.cache_data
def load_data():
    df = pd.read_csv(r'C:\Users\Namita\Documents\GitHub\spotify-data-analysis\data\SpotifyFeatures.csv')
    # Keep only relevant columns to improve speed
    df = df[['track_name','artist_name','genre','popularity','danceability','energy','valence',
             'acousticness','liveness','loudness','speechiness','tempo']]
    return df

df = load_data()

# ================= Layout =================
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# ---------------- Dataset Preview ----------------
with col1:
    st.subheader("Dataset Preview (first 100 rows)")
    st.dataframe(df.head(100))

# ---------------- Distribution Analysis ----------------
with col2:
    numerical_columns = ['popularity','acousticness','danceability','energy','valence',
                         'liveness','loudness','speechiness','tempo']
    st.sidebar.header("Data Insights")
    col = st.sidebar.selectbox("Select a column for Distribution", numerical_columns)
    st.markdown(f"<h3 style='text-align: center; font-size: 18px;'>Distribution of {col}</h3>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df[col], bins=20, kde=True, ax=ax)
    ax.set_title(f"{col} Distribution")
    st.pyplot(fig)

# ================= Analysis Functions =================
def genre_analysis(df):
    st.header("🎼 Genre Analysis")
    num_unique_genres = df['genre'].nunique()
    st.write(f"Number of Unique Genres: {num_unique_genres}")

    feature_choice = st.selectbox("Select Feature for Analysis", ["popularity", "danceability", "energy"])
    genre_counts = df['genre'].value_counts()

    st.subheader("Distribution of Genres")
    fig_genre = px.bar(genre_counts, x=genre_counts.index, y=genre_counts.values,
                       labels={"x":"Genre","y":"Count"}, title="Genre Distribution")
    st.plotly_chart(fig_genre)

    top_genre_count = st.slider("Number of Top Genres to Display", 1, num_unique_genres, 5)
    popular_genres = df.groupby('genre')[feature_choice].mean().sort_values(ascending=False).head(top_genre_count)
    st.subheader(f"Top {top_genre_count} Genres by {feature_choice.capitalize()}")
    st.write(popular_genres)

def artist_name_analysis(df):
    st.header("🎤 Artist Analysis")
    num_unique_artists = df['artist_name'].nunique()
    st.write(f"Number of Unique Artists: {num_unique_artists}")

    artist_name = st.text_input("Search for an Artist")
    if artist_name:
        filtered_df = df[df['artist_name'].str.contains(artist_name, case=False, na=False)]
        st.subheader(f"Tracks by {artist_name}")
        st.write(filtered_df[['track_name','popularity']])

def track_analysis(df):
    st.header("🎵 Track Analysis")
    track_choice = st.selectbox("Select a Track", df['track_name'].unique())
    if track_choice:
        selected_track = df[df['track_name']==track_choice]
        st.subheader(f"Details for Track: {track_choice}")
        st.write(selected_track)

        attributes = ['danceability','energy','valence']
        fig, ax = plt.subplots(figsize=(8,5))
        ax.bar(attributes,[selected_track.iloc[0][a] for a in attributes])
        ax.set_title(f"Track Attributes for {track_choice}")
        st.pyplot(fig)

def popularity_analysis(df):
    st.header("⭐ Popularity Analysis")
    st.subheader("Descriptive Statistics")
    st.write(df['popularity'].describe())

    num_bins = st.slider("Select number of bins for histogram", 5, 100, 20)
    fig_hist = px.histogram(df, x='popularity', nbins=num_bins, title="Popularity Distribution")
    st.plotly_chart(fig_hist)

    top_count = st.number_input("Top Tracks", 1, len(df), 10)
    bottom_count = st.number_input("Bottom Tracks", 1, len(df), 10)

    st.subheader(f"Top {top_count} Popular Tracks")
    top_tracks = df.nlargest(top_count,'popularity')
    fig_top = go.Figure(data=[go.Table(header=dict(values=["Track","Popularity"]),
                                       cells=dict(values=[top_tracks['track_name'],top_tracks['popularity']]))])
    st.plotly_chart(fig_top)

    st.subheader(f"Bottom {bottom_count} Less Popular Tracks")
    bottom_tracks = df.nsmallest(bottom_count,'popularity')
    fig_bottom = go.Figure(data=[go.Table(header=dict(values=["Track","Popularity"]),
                                          cells=dict(values=[bottom_tracks['track_name'],bottom_tracks['popularity']]))])
    st.plotly_chart(fig_bottom)

    st.subheader("Most Frequent Artists")
    artist_counts = df['artist_name'].value_counts().reset_index()
    artist_counts.columns = ['Artist','Track Count']
    fig_artist = px.bar(artist_counts.head(20), x='Artist', y='Track Count', title="Top 20 Artists by Track Count")
    st.plotly_chart(fig_artist)

# ================= Genre Graphs (col3) =================
with col3:
    st.sidebar.header("Genre Graphs")
    genre_avg = df.groupby('genre')[['popularity','energy','danceability']].mean().reset_index()
    graph_choice = st.sidebar.selectbox("Select Genre Graph",
        ["Average Popularity by Genre","Average Energy by Genre","Average Danceability by Genre"])

    if graph_choice=="Average Popularity by Genre":
        fig = px.bar(genre_avg, x='popularity', y='genre', orientation='h', color='popularity',
                     title='Average Popularity by Genre', color_continuous_scale='viridis')
        st.plotly_chart(fig)
    elif graph_choice=="Average Energy by Genre":
        fig = px.bar(genre_avg, x='energy', y='genre', orientation='h', color='energy',
                     title='Average Energy by Genre', color_continuous_scale='viridis')
        st.plotly_chart(fig)
    elif graph_choice=="Average Danceability by Genre":
        fig = px.bar(genre_avg, x='danceability', y='genre', orientation='h', color='danceability',
                     title='Average Danceability by Genre', color_continuous_scale='viridis')
        st.plotly_chart(fig)

# ================= 3D Scatter Plots (col4) =================
with col4:
    st.sidebar.header("3D Scatter Plots")
    scatter_choice = st.sidebar.selectbox("Select a 3D Scatter Plot",
        ["Liveness vs Popularity vs Energy","Loudness vs Popularity vs Energy","Speechiness vs Popularity vs Energy"])

    df_sample = df.sample(5000, random_state=42)  # sample for speed

    if scatter_choice=="Liveness vs Popularity vs Energy":
        fig = px.scatter_3d(df_sample, x='popularity', y='energy', z='liveness', color='liveness')
        st.plotly_chart(fig)
    elif scatter_choice=="Loudness vs Popularity vs Energy":
        fig = px.scatter_3d(df_sample, x='popularity', y='energy', z='loudness', color='loudness')
        st.plotly_chart(fig)
    elif scatter_choice=="Speechiness vs Popularity vs Energy":
        fig = px.scatter_3d(df_sample, x='popularity', y='energy', z='speechiness', color='speechiness')
        st.plotly_chart(fig)

# ================= Main =================
def main():
    st.sidebar.header("Analysis Options")
    analysis_choice = st.sidebar.selectbox("Select Analysis",
        ["Genre Analysis","Artist Name Analysis","Track Name Analysis","Popularity Analysis"])

    if analysis_choice=="Genre Analysis":
        genre_analysis(df)
    elif analysis_choice=="Artist Name Analysis":
        artist_name_analysis(df)
    elif analysis_choice=="Track Name Analysis":
        track_analysis(df)
    elif analysis_choice=="Popularity Analysis":
        popularity_analysis(df)

if __name__=="__main__":
    main()
