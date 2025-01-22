import spotipy
from loguru import logger
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from spotiplex.Home import config


class SpotifyClass:
    """Class for interacting with Spotify."""

    def __init__(self: "SpotifyClass") -> None:
        """Init for Spotify class."""
        self.spotify_id = config.spotify_config["user_id"]
        self.spotify_key = config.spotify_config["api_key"]
        self.sp = self.connect_spotify()

    def connect_spotify(self: "SpotifyClass") -> Spotify:
        """Init of spotify connection."""
        auth_manager = SpotifyClientCredentials(
            client_id=self.spotify_id,
            client_secret=self.spotify_key,
        )
        return spotipy.Spotify(auth_manager=auth_manager)

    def get_playlist_tracks(
        self: "SpotifyClass",
        playlist_id: str,
    ) -> list[tuple[str, str]]:
        """Fetch tracks from a Spotify playlist."""
        tracks: list[tuple[str, str]] = []
        try:
            results = self.sp.playlist_tracks(playlist_id)
            while results:
                tracks.extend(
                    [
                        (item["track"]["name"], item["track"]["artists"][0]["name"])
                        for item in results["items"]
                    ],
                )
                results = self.sp.next(results) if results["next"] else None
        except Exception as e:
            logger.debug(f"Error fetching tracks from Spotify: {e}")
        return tracks

    def get_playlist_name(self: "SpotifyClass", playlist_id: str) -> str | None:
        """Fetch the name of a Spotify playlist."""
        try:
            return self.sp.playlist(playlist_id, fields=["name"])["name"]
        except Exception as e:
            logger.debug(
                f"""
                Error retrieving playlist name from Spotify for playlist {playlist_id}
                """,
            )
            logger.debug(f"Error was {e}")
            return None

    def get_playlist_poster(self: "SpotifyClass", playlist_id: str) -> str | None:
        """Tries to get cover art URL and returns None if not found."""
        try:
            playlist_data = self.sp.playlist(playlist_id, fields=["images"])
        except Exception as e:
            logger.error(f"Error retrieving cover art for playlist {playlist_id}: {e}")
        if playlist_data and playlist_data["images"]:
            cover_url: str = playlist_data["images"][0]["url"]
            return cover_url
        return None
