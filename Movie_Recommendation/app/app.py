import streamlit as st
import pandas as pd
import requests
import pickle

# Load data
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# Recommendation function
def strGetRecommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# Fetch poster
def fnFetchPoster(movie_id):
    api_key = 'your_api_key'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/150"

# App layout
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Movie Recommendation System</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Choose a Movie")
    selected_movie = st.selectbox("", movies['title'].values)
    recommend_button = st.button("Show Recommendations")

if recommend_button:
    recommendations = strGetRecommendations(selected_movie)
    st.subheader(f"Top 10 movies similar to *{selected_movie}*:")

    for i in range(0, 10, 5):  # 2 rows of 5 movies
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i + 5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fnFetchPoster(movie_id)
                with col:
                    st.image(poster_url, width=160)
                    st.caption(movie_title)
