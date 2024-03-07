import requests
import urllib3
from plexapi.server import PlexServer
from confighandler import read_config


class PlexService:
    def __init__(self):
        self.config = read_config("plex")
        self.server_url = self.config.get("url")
        self.server_token = self.config.get("api_key")
        self.plex = self.connect_plex()
        self.replace = self.config.get("replace")

    def connect_plex(self):
        session = requests.Session()
        session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        return PlexServer(self.server_url, self.server_token, session=session)

    def check_tracks_in_plex(self, spotify_tracks):
        music_lib = self.plex.library.section("Music")
        plex_tracks = []
        orig_tracks = []

        for track_name, artist_name in spotify_tracks:
            artist_tracks_in_plex = music_lib.search(title=artist_name)
            if artist_tracks_in_plex:
                try:
                    for track in artist_tracks_in_plex:
                        plex_track = track.track(title=track_name)
                        if plex_track:
                            plex_tracks.append(plex_track)
                        else:
                            orig_tracks.append([track_name, "Song Not in Plex"])
                except Exception as plex_search_exception:
                    print(plex_search_exception)
            else:
                continue

        return plex_tracks

    def create_or_update_playlist(self, playlist_name, playlist_id, tracks):
        existing_playlist = self.find_playlist_by_name(playlist_name)
        if existing_playlist:
            if self.replace:
                existing_playlist.delete()
                return self.create_playlist(playlist_name, playlist_id, tracks)
            else:
                existing_playlist.addItems(tracks)
                return existing_playlist
        else:
            return self.create_playlist(playlist_name, playlist_id, tracks)

    def find_playlist_by_name(self, playlist_name):
        playlists = self.plex.playlists()
        for playlist in playlists:
            if playlist.title == playlist_name:
                return playlist
        return None

    def create_playlist(self, playlist_name, playlist_id, tracks):
        try:
            new_playlist = self.plex.createPlaylist(playlist_name, items=tracks)
            return new_playlist
        except Exception as e:
            print(f"Error creating playlist {playlist_name}: {e}")
            return None

    def list_active_streams(self):
        """Lists all users currently playing media and the media they are playing."""
        sessions = self.plex.sessions()
        if sessions:
            for session in sessions:
                user = session.usernames[0] if session.usernames else "Unknown User"
                title = session.title
                # Depending on your requirement, you might also want to include session.type (movie, episode, etc.)
                print(f"User '{user}' is playing '{title}'")
        else:
            print("No active streams.")
