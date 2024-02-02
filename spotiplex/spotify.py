import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import date
from confighandler import read_config


class SpotifyConnection:
    def __init__(self):
        self.spotifyconfig()
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





class SpotifyPlaylists:
    def __init__(self, sc, playlist_ids):
        self.spotify = sc
        self.playlist_ids = playlist_ids

    def collect_playlist_names(self):
        for playlist in self.playlist_ids:
            playlist_name = self.get_playlist_name(playlist)
            self.playlist_names.append(playlist_name)
    def get_playlist_name(self):
        try:
            playlist_data = self.spotify.playlist(self.playlist_id, fields=["name"])
            playlistname = playlist_data["name"]
            if "Discover Weekly" in playlistname or "Daily Mix" in playlistname:
                curdate = date.today()
                print("Discover")
                playlistname = f"{playlistname} {curdate}"
                print(playlistname, " is being processed")
                return playlistname
            print(playlistname, " is being processed")
            return playlistname
        except Exception as e:
            print(
                "Error retrieving playlist name. If this is unexpected, please submit a bug report."
            )
            print(e)

    def get_spotify_playlist_tracks(self, playlist_id):
        spotify_tracks = []
        try:
            results = self.sp.playlist_tracks(playlist_id)
            while results:
                for item in results["items"]:
                    track_name = item["track"]["name"]
                    artist_name = item["track"]["artists"][0]["name"]
                    spotify_tracks.append((track_name, artist_name))
                if results["next"]:
                    results = self.sp.next(results)
                else:
                    break
        except Exception as x:
            print(
                "Error fetching tracks from Spotify. See documentation for more info."
            )
            print("Error:", x)
        return spotify_tracks
