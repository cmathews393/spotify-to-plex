from .main import Spotiplex
from flask import request
import datetime

class functions:
    def __init__(self):
        self.running = True
        self.sync_started = None
        self.sync_status = "Unknown"

    def run_sync(self):
        self.sync_started = datetime.now()
        return

    def get_playlists_data(self):
        spotiplex = Spotiplex()
        playlists = spotiplex.get_data_for_playlist()
        return playlists

    def check_license(self):
        return
    def man_match(self):
        data = request.json
        track_name = data['trackName']
        artist_name = data['artistName']
        matches = Spotiplex.PlexService().manual_track_match(track_name, artist_name)
        # Convert matches to a suitable format for JSON response
        matches_json = [{"title": match.title, "artist": match.grandparentTitle} for match in matches]
        return matches_json

    def get_dashboard_data(self):
        self.service_checks()
        if self.sync_started:
            last_sync = str(self.sync_started)
        else:
            last_sync = "Unknown"
        dashboard_data = {
            "service_status": {
                "spotify_connected": self.spotify,  # Example: Check if Spotify service is connected
                "plex_connected": self.plex_conn,  # Example: Check if Plex service is connected
                "lidarr_connected": self.lidarr_conn,  # Example: Check if Lidarr service is connected
            },
            "last_sync": self.sync_started,  # Placeholder for the last sync time
            "sync_errors": [],  # Placeholder for any sync errors, if they exist
            "sync_status": self.sync_status,  # Example sync status
            "scheduled_sync": self.scheduled,  # Indicates if scheduled sync is enabled
            "next_sync_time": "2024-03-08 12:00:00",  # Placeholder for the next scheduled sync time
        }
        return dashboard_data

    def service_checks(self):
        self.spotify = False
        self.plex_conn = False
        self.lidarr_conn = False
        self.scheduled = False
        spotiplex = Spotiplex()
        if spotiplex.spotify_service:
            self.spotify = True
        if spotiplex.plex_service:
            self.plex_conn = True
        if spotiplex.lidarr_api:
            self.lidarr_conn = True
        if spotiplex.seconds_interval > 0:
            self.scheduled = True
