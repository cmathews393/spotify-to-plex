import requests
import urllib3
from plexapi.server import PlexServer
from plexapi.exceptions import BadRequest, NotFound
from confighandler import read_config
import copy


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
        print("Checking tracks in plex")
        music_lib = self.plex.library.section("Music")
        plex_tracks = []
        orig_tracks = []

        for track_name, artist_name in spotify_tracks:
            artist_tracks_in_plex = music_lib.search(title=artist_name)
            if artist_tracks_in_plex:
                for track in artist_tracks_in_plex:
                    try:
                        plex_track = track.track(title=track_name)

                        # Once we find a matching track, we want to break out of this iteration to get to the next song
                        if plex_track:
                            break
                    except NotFound:
                        # This is not really an exception, just continue
                        continue
                    except (Exception, BadRequest) as plex_search_exception:
                        print(f"Exception trying to search for title={artist_name}, title={track_name}")
                        print(plex_search_exception)
                        # While this is a fatal exception to the specific search, continue on since a subsequent match may succeed
                        continue

                if plex_track:
                    plex_tracks.append(plex_track)
                else:
                    print("Song not in plex!")
                    print(f"Found artists for '{artist_name}' ({len(artist_tracks_in_plex)})")
                    print(f"Attempted to match song '{track_name}', but could not!")
                    orig_tracks.append([track_name, "Song Not in Plex"])
            else:
                print(f"No results found for artist: {artist_name}")
                continue

        print(f"Found {len(plex_tracks)} of possible {len(spotify_tracks)} (Failed to find {len(orig_tracks)})")

        return plex_tracks

    def create_or_update_playlist(
        self, playlist_name, playlist_id, tracks
    ):
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

# Playlist is created in intervals of 300 since Plex's API will return a 414 URL TOO LONG inconsistently past that
    def create_playlist(self, playlist_name, playlist_id, tracks):
        tracks_to_add = copy.deepcopy(tracks)
        try:
            iteration_tracks = tracks_to_add[:300]
            del tracks_to_add[:300]
            new_playlist = self.plex.createPlaylist(playlist_name, items=iteration_tracks)

            while len(tracks_to_add) > 0:
                iteration_tracks = tracks_to_add[:300]
                del tracks_to_add[:300]
                new_playlist.addItems(iteration_tracks)
            return new_playlist
        except Exception as e:
            print(f"Error creating playlist {playlist_name}: {e}")
            return None
