import streamlit as st
import pickle
import pandas as pd

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,  # waits 1s, 2s, 4s, 8s... between retries
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

session = create_session()

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}".format(movie_id)
    params = {"api_key": "3061d091875062bf936ae6be19412b7d", "language": "en-US"}
    
    try:
        response = session.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster"

    

def recommand(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recomended_movie = []
    recomended_movie_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recomended_movie.append(movies.iloc[i[0]].title)
        #fetch the poster from the api 
        recomended_movie_poster.append(fetch_poster(movie_id))
    return recomended_movie , recomended_movie_poster


movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System ')

selected_movie_name = st.selectbox(
'how would you connect ?',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters  = recommand(selected_movie_name)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.subheader(names[0])
        st.image(posters[0])
    with col2:
        st.subheader(names[1])
        st.image(posters[1])
    with col3:
        st.subheader(names[2])
        st.image(posters[2])
    with col4:
        st.subheader(names[3])
        st.image(posters[3])
    with col5:
        st.subheader(names[4])
        st.image(posters[4])