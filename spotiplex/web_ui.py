from .main import Spotiplex


class functions:
    def __init__(self):
        self.running = True

    def run_sync(self):
        return

    def list_songs(self):
        return

    def check_license(self):
        return

    def get_dashboard_data(self):
        self.service_checks()
        dashboard_data = {
            "service_status": {
                "spotify_connected": self.spotify,  # Example: Check if Spotify service is connected
                "plex_connected": self.plex_conn,  # Example: Check if Plex service is connected
                "lidarr_connected": self.lidarr_conn,  # Example: Check if Lidarr service is connected
            },
            "last_sync": "2024-03-07 12:00:00",  # Placeholder for the last sync time
            "sync_errors": [],  # Placeholder for any sync errors, if they exist
            "sync_status": "Successful",  # Example sync status
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
