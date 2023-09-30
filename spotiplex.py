from plexapi.playlist import Playlist as pl
from plexapi.server import PlexServer
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib3
from decouple import config


def connect_plex():
    urllib3.disable_warnings(
        urllib3.exceptions.InsecureRequestWarning
    )  # Plex API hates SSL or something idk it was annoying
    session = requests.Session()  # Open session
    session.verify = False  # Ignore SSL errors
    PLEX_SERVER_URL = config("PLEX_URL")
    PLEX_SERVER_TOKEN = config("PLEX_TOKEN")
    plex = PlexServer(
        PLEX_SERVER_URL, PLEX_SERVER_TOKEN, session=session
    )  # Connect to Plex server
    return plex


def connect_spotify():
    SPOTIPY_CLIENT_ID = config("SPOTIFY_API_ID")
    SPOTIPY_CLIENT_SECRET = config("SPOTIFY_API_KEY")
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
        )
    )
    return sp


def extract_playlist_id(playlist_url):  # parse playlist ID from URL if applicable
    if "playlist/" in playlist_url:
        playlist_id = playlist_url.split("playlist/")[
            1
        ]  # Remove excess text if inputting URL manually and not via Lidarr
        return playlist_id
    else:
        playlist_id = playlist_url
        return playlist_id


def get_spotify_tracks(sp, playlist_id):
    try:
        results = sp.playlist_tracks(playlist_id)
    except:
        print("blerp")
    return results


def get_spotify_playlist_tracks(sp, playlist_id):
    """Get all tracks from Spotify."""
    spotify_tracks = []
    
    try:
        results = sp.playlist_tracks(playlist_id)
        
        while results:
            for item in results["items"]:
                track_name = item["track"]["name"]
                artist_name = item["track"]["artists"][0]["name"]
                spotify_tracks.append((track_name, artist_name))

            if results["next"]:
                results = sp.next(results)
            else:
                break

    except Exception as x:
        print("Error fetching tracks from Spotify. See documentation for more info.")
        print("Error:", x)

    return spotify_tracks

def check_tracks_in_plex(plex, spotify_tracks):
    """Check if the tracks from Spotify exist in Plex."""
    plex_tracks = []
    orig_tracks = []

    music = plex.library.section("Music")
    for track_name, artist_name in spotify_tracks:
        print(f"Track: {track_name}, Artist: {artist_name}")
        artist_tracks_in_plex = music.search(title=artist_name)
        
        if artist_tracks_in_plex:
            for track in artist_tracks_in_plex:
                try:
                    plex_track = track.track(title=track_name)
                    if plex_track:
                        plex_tracks.append(plex_track)
                        orig_tracks.append([track_name, artist_name])
                    else:
                        orig_tracks.append([track_name, "Song Not in Plex"])
                except Exception as e:
                    print(e)
                    orig_tracks.append([track_name, "Song Not in Plex"])
        else:
            orig_tracks.append(["Artist Not Found", "Artist Not Found"])

    return plex_tracks, orig_tracks

def get_playlist_name(sp, playlist_id):
    """Retrieve the name of the playlist for further use in create_list."""
    try:
        playlist_data = sp.playlist(playlist_id, fields=["name"])
        return playlist_data["name"]
    except Exception as e:
        print("Error retrieving playlist name. If this is unexpected, please submit a bug report.")
        print(e)
        
def make_lidarr_api_call(api_key, endpoint, params=None):
    # Add API key to header
    headers = {
        "X-Api-Key": api_key,
    }
    # Combine lidarr IP with API call
    url = f"{LIDARR_IP}{endpoint}"

    # Store response from Lidarr
    response = requests.get(url, headers=headers, params=params)
    # parse response if it exists, else send error message
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def getlidarrlists():
    api_key = LIDARR_TOKEN
    # This shouldn't change, but if it does and it stops working for you, submit a bug report and I'll fix
    endpoint = "/api/v1/importlist"

    result = make_lidarr_api_call(api_key, endpoint)
    if result:  # Checks to make sure we got a response
        playlists = []  # initialize playlist... list
        for entry in result:  # grabs each playlist
            if entry.get("listType") == "spotify" and entry.get(
                "fields"
            ):  # Check if import list is spotify sourced
                for field in entry["fields"]:  # search all fields in entry
                    if (
                        field.get("name") == "playlistIds"
                    ):  # Grab playlist ID (i.e. spotify.com/playlist/PLAYLISTID) if the field is playlistid
                        playlists.extend(field.get("value", []))
                        break
        return playlists

