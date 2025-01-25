import streamlit as st

from spotiplex.modules.confighandler import main as ch

config = ch.Config()


def main():
    st.header("Welcome to Spotiplex. Please input your API keys and settings below:")
    show_configs = st.checkbox("Show Existing Configs?")
    # Spotify Configuration
    st.subheader("Spotify Configuration")
    sp_config = ch.read_config("spotify")
    if show_configs is True:
        st.write(sp_config)
    if sp_config:
        spotify_api_key = st.text_input(
            "Spotify API Key (Currently Set)",
            type="password",
        )
        spotify_user_id = st.text_input("Spotify User ID (Currently Set)")
        if spotify_api_key and spotify_user_id:
            spotify_data = {
                "api_key": spotify_api_key,
                "user_id": spotify_user_id,
            }
            ch.write_config("spotify", data=spotify_data)
    else:
        spotify_api_key = st.text_input("Spotify API Key", type="password")
        spotify_user_id = st.text_input("Spotify User ID")
        if spotify_api_key and spotify_user_id:
            spotify_data = {
                "api_key": spotify_api_key,
                "user_id": spotify_user_id,
            }
            ch.write_config("spotify", data=spotify_data)

    # Plex Configuration
    st.subheader("Plex Configuration")
    plex_config = ch.read_config("plex")
    if show_configs is True:
        st.write(plex_config)
    if plex_config:
        plex_api_key = st.text_input("Plex API Key (Currently Set)", type="password")
        plex_url = st.text_input("Plex URL (Currently Set)")
        plex_usernames = st.text_area("Plex Usernames (Comma-separated, Currently Set)")
        if plex_api_key and plex_url and plex_usernames:
            plex_data = {
                "api_key": plex_api_key,
                "url": plex_url,
                "usernames": [user.strip() for user in plex_usernames.split(",")],
            }
            ch.write_config("plex", data=plex_data)
    else:
        plex_api_key = st.text_input("Plex API Key", type="password")
        plex_url = st.text_input("Plex URL")
        plex_usernames = st.text_area("Plex Usernames (Comma-separated)")
        if plex_api_key and plex_url and plex_usernames:
            plex_data = {
                "api_key": plex_api_key,
                "url": plex_url,
                "usernames": [user.strip() for user in plex_usernames.split(",")],
            }
            ch.write_config("plex", data=plex_data)

    # Lidarr Configuration
    st.subheader("Lidarr Configuration")
    lidarr_config = ch.read_config("lidarr")
    if show_configs is True:
        st.write(lidarr_config)
    if lidarr_config:
        lidarr_url = st.text_input("Lidarr URL (Currently Set)")
        lidarr_api_key = st.text_input(
            "Lidarr API Key (Currently Set)",
            type="password",
        )
        if lidarr_url and lidarr_api_key:
            lidarr_data = {
                "url": lidarr_url,
                "api_key": lidarr_api_key,
            }
            ch.write_config("lidarr", data=lidarr_data)
    else:
        lidarr_url = st.text_input("Lidarr URL")
        lidarr_api_key = st.text_input("Lidarr API Key", type="password")
        if lidarr_url and lidarr_api_key:
            lidarr_data = {
                "url": lidarr_url,
                "api_key": lidarr_api_key,
            }
            ch.write_config("lidarr", data=lidarr_data)

    # Generic Configuration
    st.subheader("Generic Configuration")
    generic_config = ch.read_config("spotiplex")
    if show_configs is True:
        st.write(generic_config)

    sync_interval = st.number_input(
        "Sync Interval (in minutes)",
        min_value=1,
        value=generic_config.get("sync_interval", 10),
    )
    worker_count = st.number_input(
        "Worker Count",
        min_value=1,
        value=generic_config.get("worker_count", 5),
    )
    manual_playlists_input = st.text_area(
        "Enable Manual Playlists (One playlist per line)",
        value="\n".join(generic_config.get("manual_playlists", [])),
    )
    manual_playlists = [
        playlist.strip()
        for playlist in manual_playlists_input.splitlines()
        if playlist.strip()
    ]
    lidarr_sync = st.checkbox(
        "Enable Lidarr Sync",
        value=generic_config.get("lidarr_sync", True),
    )
    cover_art_sync = st.checkbox(
        "Enable Cover Art Sync",
        value=generic_config.get("cover_art_sync", True),
    )
    playlist_author = st.checkbox(
        "Set Playlist Author",
        value=generic_config.get("playlist_author", True),
    )
    replace_existing = st.checkbox(
        "Replace Existing Playlists",
        value=generic_config.get("replace_existing", True),
    )

    if st.button("Save Configuration"):
        generic_data = {
            "sync_interval": sync_interval,
            "worker_count": worker_count,
            "manual_playlists": manual_playlists,
            "lidarr_sync": lidarr_sync,
            "cover_art_sync": cover_art_sync,
            "playlist_author": playlist_author,
            "replace_existing": replace_existing,
        }
        ch.write_config("spotiplex", data=generic_data)
        st.success("Configuration saved successfully!")


if __name__ == "__main__":
    main()
