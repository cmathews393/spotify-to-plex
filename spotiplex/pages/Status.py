import streamlit as st

from spotiplex.Home import config
from spotiplex.modules.spotify.main import SpotifyClass

st.header("Currently active playlists:")
if st.button("Clear All"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
    st.cache_data.clear()


def status():
    spotify = SpotifyClass()
    st.write(config.spotiplex_config["manual_playlists"])
    if isinstance(
        config.spotiplex_config["manual_playlists"],
        str,
    ):  # Handle case where it's saved as a single string
        playlists = [
            playlist.strip()
            for playlist in config.spotiplex_config["manual_playlists"].splitlines()
            if playlist.strip()
        ]
    elif isinstance(
        config.spotiplex_config["manual_playlists"],
        list,
    ):  # Already a list
        playlists = config.spotiplex_config["manual_playlists"]
    else:
        playlists = []
    for playlist in playlists:
        st.write(spotify.get_playlist_name(playlist))


status()

if st.button("Rerun All"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
    st.rerun()
