import streamlit as st

from spotiplex.modules.confighandler import main as ch

st.header("Welcome to Spotiplex. Please input your API keys below:")


sp_config = ch.read_config("spotify")
st.write(sp_config)
if sp_config:
    spotify_api_key = st.text_input("Spotify API Key (Currently Set)", type="password")
    spotify_user_id = st.text_input("Spotify API ID (Currently Set)")
    if spotify_api_key and spotify_user_id:
        data = {
            "api_key": spotify_api_key,
            "user_id": spotify_user_id,
        }
        ch.write_config("spotify", data=data)
else:
    password = st.text_input("Spotify API Key", type="password")
plex_api_key = st.text_input("Plex API Key", type="password")
