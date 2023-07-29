import requests
import json
api_key = ""

base_url = ""




def make_lidarr_api_call(api_key, endpoint, params=None):

    headers = {
        "X-Api-Key": api_key,
    }

    url = f"{base_url}{endpoint}"
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def lidarrtest():
    api_key = ""  # Replace with your actual Lidarr API key
    endpoint = "/api/v1/importlist"

    # Example: Get all albums

    result = make_lidarr_api_call(api_key, endpoint)
    if result:
        playlists = []
        for entry in result:
            if entry.get('listType') == 'spotify' and entry.get('fields'):
                for field in entry['fields']:
                    if field.get('name') == 'playlistIds':
                        playlists.extend(field.get('value', []))
                        break
    return playlists

playlists = lidarrtest()
print(playlists)
