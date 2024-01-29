import json
from confighandler import read_config

# test


class LidarrAPI:
    def __init__(self):
        self.config = read_config()

    def make_request(self, endpoint_path=""):
        full_url = self.base_url + endpoint_path
        response = requests.get(full_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            with open("data_file.json", "w") as file:
                json.dump(data, file, indent=4)
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def lidarrconfig(self):
        url = self.config.get("url")
        token = self.config.get("api_key")
        return url, token
