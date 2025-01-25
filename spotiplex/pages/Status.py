import streamlit as st

from spotiplex.modules.confighandler import main as ch
from spotiplex.modules.spotify.main import SpotifyClass

config = ch.Config()
st.header("Currently active playlists:")
col1, col2 = st.columns(2)
with col1:
    if st.button("Clear Cache"):
        st.cache_data.clear()
with col2:
    if st.button("Rerun All"):
        st.rerun()

if isinstance(
    config.spotiplex_config["manual_playlists"],
    str,
):
    playlists = [
        playlist.strip()
        for playlist in config.spotiplex_config["manual_playlists"].splitlines()
        if playlist.strip()
    ]
elif isinstance(
    config.spotiplex_config["manual_playlists"],
    list,
):
    playlists = config.spotiplex_config["manual_playlists"]
else:
    playlists = []


@st.cache_data()
def status(playlists: list) -> None:
    """Extract and display playlists and tracks."""
    spotify = SpotifyClass()

    for playlist in playlists:
        if (
            "37i9d" in playlist
        ):  # Unsure if this will catch all Spotify playlists, but its been consistent across all of mine
            st.write("Unable to sync")
            with st.expander("See link below"):
                st.write(
                    "https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api",
                )
        else:
            st.write(spotify.get_playlist_name(playlist))
            with st.expander("Playlist tracks:"):
                artist, title = st.columns(2)
                for track in spotify.get_playlist_tracks(playlist):
                    with st.container(border=True):
                        st.write("Artist: ", track[1])
                        st.write("Title: ", track[0])


status(playlists)
