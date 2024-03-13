import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import date
from .confighandler import read_config


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
    
    def get_playlist_data(self, playlist_id):
        playlist = self.sp.playlist(playlist_id)
    
    # Simplify the data structure for the example
        simplified_playlist = {
            "name": playlist['name'],
            "description": playlist['description'],
            "external_urls": playlist['external_urls'],
            "followers": playlist['followers']['total'],
            "images": playlist['images'],
            "tracks": {
                "total": playlist['tracks']['total'],
                "items": [{
                    "added_at": item['added_at'],
                    "track": {
                        "name": item['track']['name'],
                        "album": item['track']['album']['name'],
                        "artists": [artist['name'] for artist in item['track']['artists']],
                        "external_urls": item['track']['external_urls'],
                        "preview_url": item['track']['preview_url']
                    }
                } for item in playlist['tracks']['items']]
            }
        }
        
        return simplified_playlist


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
