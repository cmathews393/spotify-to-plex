import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from confighandler import read_config

class spotifyplaylist():
    def __init__(self):
        self.sp = self.connect_spotify()

    def spotifyconfig(self):
        self.spconfig = read_config("spotify")
        self.SPOTIPY_CLIENT_SECRET = self.spconfig.get("api_key")
        self.SPOTIPY_CLIENT_ID = self.spconfig.get("client_id")

    def connect_spotify(self):
        return spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=self.SPOTIPY_CLIENT_ID,
                client_secret=self.SPOTIPY_CLIENT_SECRET,
            )
        )

