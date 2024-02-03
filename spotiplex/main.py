from plex import PlexService
from spotify import SpotifyService
from lidarr import LidarrAPI as lapi
from confighandler import read_config, write_config
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import schedule
import time
import os


class Spotiplex:
    def __init__(self):
        self.config = read_config("spotiplex")
        self.first_run = self.config.get("first_run")
        if (
            self.first_run is None
            or self.first_run == "True"
            or Spotiplex.is_running_in_docker()
        ):
            Spotiplex.configurator(self)
        self.spotify_service = SpotifyService()
        self.plex_service = PlexService()
        self.lidarr_api = lapi()

        self.lidarr_sync = (self.config.get("lidarr_sync", "false")).lower()
        self.plex_users = self.config.get("plex_users")
        self.user_list = self.plex_users.split(",") if self.plex_users else []
        self.worker_count = int(self.config.get("worker_count"))
        self.replace_existing = self.config.get("replace_existing")
        self.seconds_interval = int(self.config.get("seconds_interval"))
        if self.lidarr_sync == "true":
            self.sync_lists = self.lidarr_api.get_lidarr_playlists()
        else:
            self.sync_lists = self.config.get("manual_playlists")
        currentuser = self.plex_service.plex.myPlexAccount().username.lower()
        if currentuser in self.user_list:
            self.user_list.remove(currentuser)

    def process_for_user(self, user):
        if user:
            self.plex_service.plex = self.plex_service.plex.switchUser(user)
            print(f"Processing playlists for user: {user}")

        with ThreadPoolExecutor(max_workers=self.worker_count) as executor:
            futures = [
                executor.submit(
                    self.process_playlist,
                    playlist,
                    self.plex_service,
                    self.spotify_service,
                    self.replace_existing,
                )
                for playlist in self.sync_lists
            ]

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Thread resulted in an error: {e}")

    def is_running_in_docker():
        return os.path.exists("/.dockerenv")

    def run(self):
        for user in self.user_list:
            self.process_for_user(user)

        if self.seconds_interval > 0:
            schedule.every(self.seconds_interval).seconds.do(self.run)
            while True:
                schedule.run_pending()
                time.sleep(1)

    def extract_playlist_id(playlist_url):  # parse playlist ID from URL if applicable
        if "?si=" in playlist_url:
            playlist_url = playlist_url.split("?si=")[0]

        return (
            playlist_url.split("playlist/")[1]
            if "playlist/" in playlist_url
            else playlist_url
        )

    def process_playlist(
        self, playlists, plex_service, spotify_service, replace_existing
    ):
        for playlist in playlists:
            try:
                playlist_id = Spotiplex.extract_playlist_id(playlist)
                print(playlist_id)
                playlist_name = spotify_service.get_playlist_name(playlist_id)
                spotify_tracks = spotify_service.get_playlist_tracks(playlist_id)
                plex_tracks = plex_service.check_tracks_in_plex(spotify_tracks)
                plex_service.create_or_update_playlist(
                    playlist_name, playlist_id, plex_tracks
                )
                print(f"Processed playlist '{playlist_name}'.")
            except Exception as e:
                print(f"Error processing playlist '{playlist}':", e)

    def configurator(self):
        # Config for Spotiplex
        if Spotiplex.is_running_in_docker():
            # Fetching configuration from environment variables if running in Docker
            spotiplex_config = {
                "lidarr_sync": os.environ.get("SPOTIPLEX_LIDARR_SYNC", "True"),
                "plex_users": os.environ.get("USERS", ""),
                "worker_count": int(os.environ.get("WORKERS", 1)),
                "seconds_interval": int(os.environ.get("INTERVAL", 86400)),
                "manual_playlists": os.environ.get(
                    "SPOTIPLEX_MANUAL_PLAYLISTS", "False"
                ),
            }
            write_config("spotiplex", spotiplex_config)

            spotify_config = {
                "client_id": os.environ.get("SPOTIFY_API_ID", ""),
                "api_key": os.environ.get("SPOTIFY_API_KEY", ""),
            }
            write_config("spotify", spotify_config)

            plex_config = {
                "url": os.environ.get("PLEX_URL", ""),
                "api_key": os.environ.get("PLEX_TOKEN", ""),
                "replace": os.environ.get("REPLACE", "False"),
            }
            write_config("plex", plex_config)

            lidarr_config = {
                "url": os.environ.get("LIDARR_IP", ""),
                "api_key": input("LIDARR_TOKEN", ""),
            }
            write_config("lidarr", lidarr_config)

            print("Configuration set from environment variables.")
        else:
            print(
                "Welcome to Spotiplex! It seems this is your first run of the application, please enter your configuration variables below. Press Enter to continue..."
            )
            spotiplex_config = {
                "lidarr_sync": input("Enter Lidarr sync option (True/False): "),
                "plex_users": input("Enter comma-separated Plex user names: "),
                "worker_count": int(
                    input(
                        "Enter the number of worker threads (Not recommened to exceed core count. 5 is usually a good value.): "
                    )
                ),
                "seconds_interval": int(
                    input(
                        "Enter the interval in seconds for scheduling, set to 0 if you don't want the script to repeat: "
                    )
                ),
                "manual_playlists": input("Enter manual playlists (True/False): "),
            }

            # Config for SpotifyService
            spotify_config = {
                "client_id": input("Enter Spotify client ID: "),
                "api_key": input("Enter Spotify API key: "),
            }
            write_config("spotify", spotify_config)

            # Config for PlexService
            plex_config = {
                "url": input("Enter Plex server URL: "),
                "api_key": input("Enter Plex API key: "),
                "replace": input("Replace existing Plex data? (True/False): "),
            }
            write_config("plex", plex_config)

            lidarr_config = {
                "url": input("Enter Lidarr URL: "),
                "api_key": input("Enter Lidarr API Key: "),
            }
            write_config("lidarr", lidarr_config)

            spotiplex_config["first_run"] = "False"
            write_config("spotiplex", spotiplex_config)

            print("Configuration complete!")


def main():
    spotiplex = Spotiplex()
    spotiplex.run()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
