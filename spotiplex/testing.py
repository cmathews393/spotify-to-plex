from spotify2 import SpotifyService
from plex import PlexService



spotify_service = SpotifyService()
plex_service = PlexService()

playlist_id = "https://open.spotify.com/playlist/37i9dQZF1EQn4jwNIohw50"
spotify_tracks = spotify_service.get_playlist_tracks(playlist_id)
playlist_name = spotify_service.get_playlist_name(playlist_id)

plex_tracks = plex_service.check_tracks_in_plex(spotify_tracks)
plex_service.create_or_update_playlist(playlist_name, playlist_id, plex_tracks)