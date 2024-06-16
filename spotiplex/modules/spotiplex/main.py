from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from loguru import logger

from spotiplex.config import (
    Config,
)
from spotiplex.modules.lidarr.main import LidarrClass
from spotiplex.modules.plex.main import PlexClass
from spotiplex.modules.spotify.main import SpotifyClass


class Spotiplex:
    """Class to hold Spotiplex functions."""

    def __init__(self, lidarr: bool | None, playlist_id: str | None):
        self.spotify_service = SpotifyClass()
        self.plex_service = PlexClass()
        self.user_list = self.get_user_list()
        self.default_user: str = self.plex_service.plex.myPlexAccount().username
        self.worker_count: int = Config.WORKER_COUNT
        self.replace_existing = Config.PLEX_REPLACE
        if not playlist_id:
            self.lidarr_service = LidarrClass()
            self.lidarr = lidarr
            self.get_sync_lists()

    def get_user_list(self) -> list[str]:
        """Gets user list and makes it into a usable list."""
        plex_users = Config.PLEX_USERS
        user_list: list[str] = plex_users.split(",") if plex_users else []
        if not user_list:
            user_list.append(self.default_user)
        logger.debug(f"Users to process: {user_list}")
        return user_list

    def get_sync_lists(self) -> None:
        """Runs lidarr function to get lidarr lists or splits manual playlists to list."""
        if self.lidarr:
            self.sync_lists = self.lidarr_service.playlist_request()
        self.sync_lists = Config.MANUAL_PLAYLISTS.split(",")

    def process_for_user(self, user: str) -> None:
        logger.debug(f"Processing for user {user}")
        self.plex_service.plex = (
            self.plex_service.plex
            if user == self.default_user
            else self.plex_service.plex.switchUser(user)
        )

        with ThreadPoolExecutor(max_workers=self.worker_count) as executor:
            futures = [
                executor.submit(self.process_playlist, playlist)
                for playlist in self.sync_lists
            ]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.debug(f"Thread resulted in an error: {e}")

    def run(self) -> None:
        for user in self.user_list:
            self.process_for_user(user)

    def process_playlist(self, playlist: str) -> None:
        try:
            playlist_id = self.extract_playlist_id(playlist)
            playlist_name: str = self.spotify_service.get_playlist_name(playlist_id)
            if "Discover Weekly" in playlist_name:
                current_date = datetime.now().strftime("%B %d")
                playlist_name = f"{playlist_name} {current_date}"
            if "Daily Mix" in playlist_name:
                current_date = datetime.now().strftime("%B %d")
                playlist_name = f"{playlist_name} {current_date}"
            spotify_tracks = self.spotify_service.get_playlist_tracks(playlist_id)
            plex_tracks = self.plex_service.match_spotify_tracks_in_plex(spotify_tracks)
            self.plex_service.create_or_update_playlist(
                playlist_name,
                playlist_id,
                plex_tracks,
            )
            logger.debug(f"Processed playlist '{playlist_name}'.")
        except Exception as e:
            logger.debug(f"Error processing playlist '{playlist}': {e}")

    @staticmethod
    def extract_playlist_id(playlist_url: str) -> str:
        """Get playlist ID from URL if needed."""
        if "?si=" in playlist_url:
            playlist_url = playlist_url.split("?si=")[0]
        return (
            playlist_url.split("playlist/")[1]
            if "playlist/" in playlist_url
            else playlist_url
        )
