import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity  # Import cosine_similarity


def fetch_poster(tmdb_id):
    # TMDB API endpoint to get TV show details
    api_key = 'efb59ecf008d5d2e560b9f50416b9aac'
    url = f'https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Return the full poster path
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data['poster_path'] else None
    else:
        return None


def recommend(drama):
    # Get index of the selected drama
    drama_index = dramas[dramas['Name'] == drama].index[0]

    # Get similarity distances for the selected drama
    distances = similarity[drama_index]

    # Get indices of the most similar dramas, excluding the selected drama itself
    dramas_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_dramas = []
    # Include the selected drama
    recommended_dramas.append(drama)  # Add the selected drama itself
    for i in dramas_list:
        recommended_dramas.append(dramas.iloc[i[0]].Name)

    return recommended_dramas


# Load the dramas and similarity data
dramas_dict = pickle.load(open('dramas_dict.pkl', 'rb'))
dramas = pd.DataFrame(dramas_dict)

# Create a simple name similarity matrix
name_similarity = pd.Series(dramas['Name']).str.get_dummies(sep=' ').dot(
    pd.Series(dramas['Name']).str.get_dummies(sep=' ').T)
similarity = cosine_similarity(name_similarity)

# Streamlit application
st.title('K-Drama Recommender System')

# Select box for selecting a drama name
selected_drama_name = st.selectbox(
    'Choose a K-drama to get recommendations:',
    dramas['Name'].values
)

# Button to trigger the recommendation
if st.button('Recommend'):
    recommendations = recommend(selected_drama_name)
    st.write("Recommended Dramas:")

    # Create a row of columns to display posters side by side
    cols = st.columns(len(recommendations))

    for i, drama in enumerate(recommendations):
        # Fetch TMDB ID for the selected drama
        tmdb_id = dramas.loc[dramas['Name'] == drama, 'tmdb_id'].values[0]
        # Fetch the poster
        poster_url = fetch_poster(tmdb_id)

        with cols[i]:  # Place the poster in the respective column
            st.image(poster_url, width=100)  # Display the poster with a width of 100 pixels
            st.write(drama)  # Display the drama name below the poster






