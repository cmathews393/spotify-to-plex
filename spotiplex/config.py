import os

from spotiplex.modules.confighandler.main import read_config

"""
We're gonna ignore the error about Constant Redefined.
Might be improper but the constants are NOT being redefined imo.
See this for reference: https://github.com/microsoft/pyright/issues/5265
"""


class Config:
    """Generic Config class to pull environment vars."""

    if os.environ.get("DOCKER"):
        SPOTIFY_API_KEY = os.environ.get("SPOTIFY_API_KEY")
        SPOTIFY_API_ID = os.environ.get("SPOTIFY_API_ID")

        PLEX_API_KEY = os.environ.get("PLEX_API_KEY")
        PLEX_SERVER_URL = os.environ.get("PLEX_SERVER_URL")
        PLEX_REPLACE = os.environ.get("REPLACE")

        LIDARR_API_KEY = os.environ.get("LIDARR_API_KEY")
        LIDARR_API_URL = os.environ.get("LIDARR_API_URL")

        PLEX_USERS = os.environ.get("PLEX_USERS")
        WORKER_COUNT: int = int(os.environ.get("WORKER_COUNT", 10))
        SECONDS_INTERVAL = int(os.environ.get("SECONDS_INTERVAL", 60))
        MANUAL_PLAYLISTS: str = os.environ.get("MANUAL_PLAYLISTS", "None")
        LIDARR_SYNC = os.environ.get("LIDARR_SYNC", "false")
        FIRST_RUN = os.environ.get("FIRST_RUN", "False")
    else:
        spotify_config = read_config("spotify")
        plex_config = read_config("plex")
        lidarr_config = read_config("lidarr")
        spotiplex_config = read_config("spotiplex")

        SPOTIFY_API_KEY = spotify_config.get("api_key")
        SPOTIFY_API_ID = spotify_config.get("client_id")

        PLEX_API_KEY = plex_config.get("api_key")
        PLEX_SERVER_URL = plex_config.get("url")
        PLEX_REPLACE = plex_config.get("replace")

        LIDARR_API_KEY = lidarr_config.get("api_key")
        LIDARR_API_URL = lidarr_config.get("url")

        PLEX_USERS = spotiplex_config.get("plex_users")
        WORKER_COUNT: int = int(spotiplex_config.get("worker_count", 10))
        SECONDS_INTERVAL = int(spotiplex_config.get("seconds_interval", 60))
        MANUAL_PLAYLISTS: str = spotiplex_config.get("manual_playlists", "None")
        LIDARR_SYNC = spotiplex_config.get("lidarr_sync", "false")
        FIRST_RUN = spotiplex_config.get("first_run", "False")
