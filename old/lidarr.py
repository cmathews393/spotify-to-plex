import json
from confighandler import read_config
import requests
# test


class LidarrAPI:
    def __init__(self):
        self.config = read_config("lidarr")
        self.base_url = self.config.get("url")
        self.api_key = self.config.get("api_key")
        self.headers = {"X-Api-Key": self.api_key}

    def make_request(self, endpoint_path=""):
        full_url = self.base_url + endpoint_path
        try:
            response = requests.get(full_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            with open("data_file.json", "w") as file:
                json.dump(data, file, indent=4)
            return data
        except requests.RequestException as e:
            print(f"Error during request: {e}")
            return None

    def get_lidarr_playlists(self):
        result = self.make_request(
            endpoint_path="/api/v1/importlist"
        )  # Specify the actual endpoint path for Lidarr API
        playlists = []

        if result:
            for entry in result:
                if entry.get("listType") == "spotify":
                    playlists.extend(
                        [
                            field.get("value", [])
                            for field in entry.get("fields", [])
                            if field.get("name") == "playlistIds"
                        ]
                    )

        return playlists
