import requests
import urllib3
from plexapi.server import PlexServer
from .confighandler import read_config
from concurrent.futures import ThreadPoolExecutor, as_completed
from fuzzywuzzy import process, fuzz


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
    
    def manual_track_match(self, track_name, artist_name):
        music_lib = self.plex.library.section("Music")
        print(f"No automatic match found for: {track_name} by {artist_name}")

        # Fuzzy search for artist in Plex
        artist_matches = process.extract(
            artist_name,
            [artist.title for artist in music_lib.searchArtists()],
            scorer=fuzz.token_set_ratio,
            limit=5
        )

        print("Top artist matches:")
        for i, (artist_match, score) in enumerate(artist_matches, 1):
            print(f"{i}. {artist_match} (score: {score})")
        artist_selection = input("Select the correct artist by number (or enter to skip): ")
        
        if artist_selection.isdigit():
            selected_artist_name = artist_matches[int(artist_selection)-1][0]
            artist_object = music_lib.searchArtists(title=selected_artist_name)[0]

            # List tracks for the selected artist
            print(f"Tracks by {selected_artist_name}:")
            tracks = artist_object.tracks()
            for i, track in enumerate(tracks, 1):
                print(f"{i}. {track.title}")

            track_selection = input("Select the correct track by number: ")
            if track_selection.isdigit():
                selected_track = tracks[int(track_selection)-1]
                return selected_track
        return None

    def fuzzy_search_single_track(self, track_info, threshold=80):
        track_name, artist_name = track_info
        music_lib = self.plex.library.section("Music")
        in_plex = False

        # Fuzzy search for artist
        artist_matches = process.extractOne(
            artist_name,
            [artist.title for artist in music_lib.searchArtists()],
            scorer=fuzz.token_set_ratio,
        )
        if artist_matches and artist_matches[1] > threshold:
            matched_artist_name = artist_matches[0]
            artist_objects = music_lib.searchArtists(title=matched_artist_name)

            for artist in artist_objects:
                tracks = artist.tracks()
                # Fuzzy search for track within the artist's tracks
                track_matches = process.extractOne(
                    track_name,
                    [track.title for track in tracks],
                    scorer=fuzz.token_set_ratio,
                )

                if track_matches and track_matches[1] > threshold:
                    in_plex = True
                    break  # Track found, no need to continue searching

        return track_name, artist_name, in_plex

    def fuzzy_exists_in_plex(self, spotify_tracks, threshold=80, max_workers=10):
        track_statuses = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a future for each spotify track
            future_to_track = {
                executor.submit(
                    self.fuzzy_search_single_track, track_info, threshold
                ): track_info
                for track_info in spotify_tracks
            }

            for future in as_completed(future_to_track):
                print("processing track")
                track_info = future_to_track[future]
                try:
                    result = future.result()
                    track_statuses.append(result)
                except Exception as exc:
                    print(f"{track_info} generated an exception: {exc}")

        return track_statuses

    def exists_in_plex(self, spotify_tracks):
        music_lib = self.plex.library.section("Music")
        track_statuses = []

        for track_name, artist_name in spotify_tracks:
            in_plex = False

            # Step 1: Search for artist objects by name
            artist_objects = music_lib.searchArtists(title=artist_name)

            # Step 2: For each artist, check if they have a track matching the track_name
            for artist in artist_objects:
                tracks = artist.tracks()
                for track in tracks:
                    if track.title.lower() == track_name.lower():
                        in_plex = True
                        break
                if in_plex:
                    break  # Found the track, no need to continue

            track_statuses.append((track_name, artist_name, in_plex))

        return track_statuses


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
