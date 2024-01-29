import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import date
from confighandler import read_config


class SpotifyConnector:
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

    def extract_playlist_id(self, playlist_url):
        if "?si=" in playlist_url:
            playlist_url = playlist_url.split("?si=")[0]
        return (
            playlist_url.split("playlist/")[1]
            if "playlist/" in playlist_url
            else playlist_url
        )

    def get_playlist_name(self, playlist_id):
        try:
            playlist_data = self.sp.playlist(playlist_id, fields=["name"])
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

    def get_spotify_tracks(self, playlist_id):
        try:
            results = self.sp.playlist_tracks(playlist_id)
        except Exception as exception1:
            name = self.get_playlist_name(
                self.sp, playlist_id
            )  # Assuming get_playlist_name is imported
            print(
                f"Error getting tracks for playlist {name}, playlistID: {playlist_id}"
            )
            print(exception1)
        return results

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
