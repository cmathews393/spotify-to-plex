import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import date
from confighandler import read_config


class SpotifyService:
    def __init__(self):
        self.config = read_config("spotify")
        self.client_id = self.config.get("client_id")
        self.client_secret = self.config.get("api_key")
        self.sp = self.connect_spotify()

    def connect_spotify(self):
        auth_manager = SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret
        )
        return spotipy.Spotify(auth_manager=auth_manager)

    def get_playlist_tracks(self, playlist_id):
        tracks = []
        try:
            results = self.sp.playlist_tracks(playlist_id)
            while results:
                tracks.extend(
                    [
                        (item["track"]["name"], item["track"]["artists"][0]["name"])
                        for item in results["items"]
                    ]
                )
                results = self.sp.next(results) if results["next"] else None
        except Exception as e:
            print(f"Error fetching tracks from Spotify: {e}")
        return tracks

    def get_playlist_name(self, playlist_id):
        try:
            playlist_data = self.sp.playlist(playlist_id, fields=["name"])
            name = playlist_data["name"]
            if "Discover Weekly" in name or "Daily Mix" in name:
                name = f"{name} {date.today()}"
            return name
        except Exception as e:
            print(f"Error retrieving playlist name: {e}")
            return None
