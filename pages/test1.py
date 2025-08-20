import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Random Joke Generator", layout="centered")

st.title("😂 Random Joke Generator")

if st.button("Get a Joke"):
    try:
        # Using requests to fetch joke API
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke = response.json()
            st.success(joke["setup"])
            st.info(joke["punchline"])
        else:
            st.error("Failed to fetch a joke. Try again!")
    except Exception as e:
        st.error(f"Error: {e}")
