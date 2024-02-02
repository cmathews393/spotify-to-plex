from plex import PlexConnector as pc
from plex import PlexPlaylists as pplaylists
from spotify import SpotifyConnection as sc
from spotify import SpotifyPlaylists as splaylists
from lidarr import LidarrAPI as lapi
from confighandler import read_config
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import schedule
import time


class Spotiplex:
    def __init__(self):
        self.config = read_config("spotiplex")
        self.lidarr_sync = self.config.get("lidarr_sync")
        self.plex_users = self.config.get("plex_users")
        self.user_list = self.plex_users.split(",") if self.plex_users else []
        self.worker_count = self.config.get("worker_count")
        self.replace_existing = self.config.get("replace_existing")
        self.seconds_interval = self.config.get("seconds_interval")
        self.manual_playlists = self.config.get("manual_playlists")
        self.plex = pc.connect_plex()
        self.spotify = sc.sp()
        self.lidarr_playlists = lapi.get_lidarr_playlists()
        currentuser = self.plex.user().lower()
        if currentuser in self.user_list:
            self.user_list.remove(currentuser)

    def process_for_user(self, user):
        if user:
            self.plex = self.plex.switchUser(user)
            print(f"Processing playlists for user: {user}")

        with ThreadPoolExecutor(max_workers=self.worker_count) as executor:
            futures = [
                executor.submit(
                    self.process_playlist,
                    playlist,
                    self.plex,
                    self.spotify,
                    self.replace_existing,
                )
                for playlist in self.lidarr_playlists
            ]

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Thread resulted in an error: {e}")

    def run(self):
        for user in self.plex_users:
            self.process_for_user(user)

        if self.seconds_interval > 0:
            schedule.every(self.seconds_interval).seconds.do(self.run)
            while True:
                schedule.run_pending()
                time.sleep(1)


    def extract_playlist_id(self, playlist_url):
        if "?si=" in playlist_url:
            playlist_url = playlist_url.split("?si=")[0]
        return (
            playlist_url.split("playlist/")[1]
            if "playlist/" in playlist_url
            else playlist_url
        )
    
    def process_playlist(self, playlist, plex, spotify, replace_existing):
        try:
            playlist_id = self.extract_playlist_id(playlist)
            print(playlist_id)
            playlist_name = sc.get_playlist_name(sp, playlist_id)
            spotify_tracks = get_spotify_playlist_tracks(sp, playlist_id)
            plex_tracks, _ = check_tracks_in_plex(plex, spotify_tracks)
            create_list(plex, plex_tracks, playlist_name, playlist_id, replace)
            print(f"Processed playlist '{playlist_name}'.")
        except Exception as e:
            print(f"Error processing playlist '{playlist}':", e)

def main():
    spotiplex = Spotiplex()
    spotiplex.run()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
