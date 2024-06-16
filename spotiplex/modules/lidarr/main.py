import httpx
from spotiplex.config import Config
from loguru import logger


class LidarrClass:
    """Class to contain Lidarr functions."""

    def __init__(self: "LidarrClass") -> None:
        """Class init for LidarrClass"""
        self.url = Config.LIDARR_API_URL
        self.api_key = Config.LIDARR_API_KEY
        self.headers = {"X-Api-Key": self.api_key}

    def lidarr_request(
        self: "LidarrClass",
        endpoint_path: str,
    ) -> httpx.Response | None:
        """Generic request function."""
        try:
            response = httpx.get(url=f"{self.url}{endpoint_path}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.debug(f"Error during request: {e}")
            return None

    def playlist_request(self: "LidarrClass") -> list | None:
        """Request and process playlists from Lidarr."""
        endpoint = "/api/v1/importlist"
        raw_playlists = self.lidarr_request(endpoint_path=endpoint)

        if raw_playlists:
            return [
                field.get("value", [])
                for entry in raw_playlists
                if entry.get("listType") == "spotify"
                for field in entry.get("fields", [])
                if field.get("name") == "playlistIds"
            ]

        else:
            logger.debug("No playlists found!")
            return None
