class LidarrAPI:
    def __init__(self):
        self.RADARR_IP = "http://192.168.1.160:7878"
        self.RADARR_TOKEN = "2e842c75b67d46a7bd234bbbd3f66568"
        self.RADARR_ENDPOINT = read_config("RADARR_ENDPOINT", default="/api/v3/")
        self.headers = {"X-Api-Key": self.RADARR_TOKEN}
        self.base_url = f"{self.RADARR_IP}{self.RADARR_ENDPOINT}"

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