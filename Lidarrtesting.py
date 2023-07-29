import requests
import json
api_key = "cbd15faabd1a4f5e964c11f475eb51ae"

base_url = "http://192.168.1.160:8686"




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


if __name__ == "__main__":
    api_key = "cbd15faabd1a4f5e964c11f475eb51ae"  # Replace with your actual Lidarr API key
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
                    print (playlists)
