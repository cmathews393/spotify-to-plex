import requests
import urllib3
from confighandler import read_config
from plexapi.server import PlexServer
from plexapi.playlist import Playlist


class PlexConnector:
    def __init__(self):
        self.config = read_config("plex")  # Call read_config directly
        self.plex_connection = self.create_plex_session()

    def plex_config(self):
        url = self.config.get("url")
        token = self.config.get("api_key")
        return url, token

    def create_plex_session(self):
        url, token = self.plex_config()
        session = requests.Session()
        session.verify = False  # Ignore SSL errors
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        return PlexServer(url, token, session=session)


class PlexTracks:
    def __init__(self, plexcon, spotify_tracks):
        self.music = plexcon.library.section("Music")
        self.spotify_tracks = spotify_tracks
        

    def check_tracks_in_plex(self):
        """Check if the tracks from Spotify exist in Plex."""
        plex_tracks = []
        music = self.plex.library.section("Music")
        for track_name, artist_name in self.spotify_tracks:
            # print(f"Track: {track_name}, Artist: {artist_name}")
            self.artist_tracks_in_plex = music.search(title=artist_name)
            if self.artist_tracks_in_plex:
                try:
                    for track in self.artist_tracks_in_plex:
                        plex_track = track.track(title=track_name)
                        if plex_track:
                            plex_tracks.append(plex_track)
                except Exception as plex_search_error:
                    print(plex_search_error)
                    continue
            else:
                print("Artist not Found")
                continue
        return plex_tracks

class PlexPlaylists:
    def __init__(self, plexuser, plextracks, replace):
        self.plex_playlists = plexuser.playlists()
        
        


def create_list(plexuser, plextracks, playlist_name, playlist_id, replace):
    plexconn = plexuser
    plexplaylist_id = next(
        (
            playlist.ratingKey
            for playlist in plexconn.playlists()
            if playlist_name in playlist.title
        ),
        None,
    )

    if plexplaylist_id:  # If playlist exists
        print(f"Playlist found, matching and updating: {playlist_name}")
        try:
            if replace is True:
                existingtracks = plexconn.fetchItem(plexplaylist_id).items()
                plextracks.extend(existingtracks)
                oldplaylist = plexconn.playlist(title=playlist_name)
                print(oldplaylist)
                oldplaylist.delete()
                plex_playlist = plexconn.createPlaylist(
                    title=playlist_name, items=plextracks
                )
                plex_playlist.edit(
                    title=playlist_name,
                    summary=f"Synced from Spotify Playlist '{playlist_name}' Link: https://open.spotify.com/playlist/{playlist_id}",
                )
                # mixins > add poster?
            else:
                plexconn.fetchItem(plexplaylist_id).addItems(plextracks)
            # print(f"Playlist '{playlist_name}' synchronized with Spotify")
            return plexplaylist_id
        except Exception as e:
            print(
                f"Playlist {playlist_id} appears to match existing, but an issue occurred while updating."
            )
            print(e)

    else:  # If playlist doesn't exist
        try:
            plex_playlist = plexconn.createPlaylist(
                title=playlist_name, items=plextracks
            )
            if plex_playlist:
                print(f"Playlist '{playlist_name}' created successfully on Plex.")
            else:
                print("Failed to create the playlist.")
                return 0
        except Exception:
            print("Creation failed. Ensure there are tracks in your playlist.")
