import datetime

import httpx
from loguru import logger
from plexapi.exceptions import BadRequest, NotFound
from plexapi.playlist import Playlist  # Typing
from plexapi.server import PlexServer

from spotiplex.config import Config


class PlexClass:
    """Class to contain Plex functions."""

    def __init__(self: "PlexClass") -> None:
        """Init for Plex class to set up variables and initiate connection."""
        self.plex_url = Config.PLEX_SERVER_URL
        self.plex_key = Config.PLEX_API_KEY
        self.replacement_policy = Config.PLEX_REPLACE
        self.plex = self.connect_plex()

    def connect_plex(self: "PlexClass") -> PlexServer:
        """Simple function to initiate Plex Server connection."""
        session = httpx.Client(verify=False)  # noqa: S501    Risk is acceptabl for me, feel free to require HTTPS, not a requirement of this app
        return PlexServer(self.plex_url, self.plex_key, session=session)

    def match_spotify_tracks_in_plex(
        self: "PlexClass",
        spotify_tracks: list[tuple[str, str]],
    ) -> list:
        """Match Spotify tracks in Plex library and provide a summary of the import."""
        logger.debug("Checking tracks in plex...")
        matched_tracks = []
        missing_tracks = []
        total_tracks = len(spotify_tracks)
        music_library = self.plex.library.section("Music")

        for track_name, artist_name in spotify_tracks:
            artist_tracks_in_plex = music_library.search(title=artist_name)
            if not artist_tracks_in_plex:
                logger.debug(f"No results found for artist: {artist_name}")
                missing_tracks.append((track_name, artist_name))
                continue

            try:
                plex_track = next(
                    (
                        track.track(title=track_name)
                        for track in artist_tracks_in_plex
                        if track.track(title=track_name)
                    ),
                    None,
                )
            except NotFound:
                logger.debug(
                    f"Track '{track_name}' by '{artist_name}' not found in Plex.",
                )
                plex_track = None
            except (Exception, BadRequest) as plex_search_exception:
                logger.debug(
                    f"Exception trying to search for artist '{artist_name}', track '{track_name}': {plex_search_exception}",
                )
                plex_track = None

            if plex_track:
                matched_tracks.append(plex_track)
            else:
                logger.debug("Song not in Plex!")
                logger.debug(
                    f"Found artists for '{artist_name}' ({len(artist_tracks_in_plex)})",
                )
                logger.debug(f"Attempted to match song '{track_name}', but could not!")
                missing_tracks.append((track_name, artist_name))

        success_percentage = (
            (len(matched_tracks) / total_tracks) * 100 if total_tracks else 0
        )
        logger.debug(
            f"We successfully found {len(matched_tracks)}/{len(spotify_tracks)} or {success_percentage:.2f}% of the tracks.",
        )
        logger.debug(f"We are missing these tracks: {missing_tracks}")
        return matched_tracks

    def create_playlist(
        self: "PlexClass",
        playlist_name: str,
        playlist_id: str,
        tracks: list,
    ) -> Playlist | None:
        """Create a playlist in Plex with the given tracks."""
        now = datetime.datetime.now()
        try:
            iteration_tracks = tracks[:300]
            del tracks[:300]  # Delete should be lower impact than sliciing

            new_playlist: Playlist = self.plex.createPlaylist(
                playlist_name,
                items=iteration_tracks,
            )
            new_playlist.editSummary(
                summary=f"Playlist autocreated with Spotiplex on {now.strftime('%m/%d/%Y')}. Source is Spotify, Playlist ID: {playlist_id}",
            )

            while tracks:
                iteration_tracks = tracks[:300]
                del tracks[:300]  # Delete should be lower impact than sliciing
                new_playlist.addItems(iteration_tracks)

        except Exception as e:
            logger.debug(f"Error creating playlist {playlist_name}: {e}")
            return None
        else:
            return new_playlist

    def update_playlist(
        self: "PlexClass",
        existing_playlist: Playlist,
        playlist_id: str,
        tracks: list,
    ) -> Playlist:
        """Update an existing playlist in Plex."""
        now = datetime.datetime.now()
        if self.replacement_policy is not False and self.replacement_policy is not None:
            existing_playlist.delete()
            return self.create_playlist(
                existing_playlist.title,
                playlist_id,
                tracks,
            )
        else:
            existing_playlist.editSummary(
                summary=f"Playlist updated by Spotiplex on  {now.strftime('%m/%d/%Y')},. Source is Spotify, Playlist ID: {playlist_id}",
            )
            if len(tracks) > 0:
                existing_playlist.addItems(tracks)
            return existing_playlist

    def find_playlist_by_name(self, playlist_name: str) -> Playlist | None:
        """Find a playlist by name in Plex."""
        return next(
            (
                playlist
                for playlist in self.plex.playlists()
                if playlist_name in playlist.title
            ),
            None,
        )

    def create_or_update_playlist(
        self,
        playlist_name: str,
        playlist_id: str,
        tracks: list,
    ) -> Playlist | None:
        """Create or update a playlist in Plex."""
        existing_playlist = self.find_playlist_by_name(playlist_name)
        if existing_playlist is not None and tracks:
            return self.update_playlist(existing_playlist, playlist_id, tracks)
        if tracks:
            return self.create_playlist(playlist_name, playlist_id, tracks)
        return None
