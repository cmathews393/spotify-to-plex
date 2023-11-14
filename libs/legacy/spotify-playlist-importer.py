import plexapi
from plexapi.playlist import Playlist as pl
from plexapi.server import PlexServer
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib3


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)  # Plex API hates SSL or something idk it was annoying

SPOTIPY_CLIENT_ID = input("Spotify Client ID: ")
SPOTIPY_CLIENT_SECRET = input("Spotify Secret: ")
keepgoing = False  # Used later for loop
lidarrimport = False  # Used later for loop
PLEX_SERVER_TOKEN = input("PLEX Server Token: ")
PLEX_SERVER_URL = input(
    "Server URL, include http(s) and port, eg https://192.168.1.2:32400: "
)
LIDARR_IP = input("If desired, enter Lidarr IP, include HTTP and port number: ")
LIDARR_TOKEN = input("If desired, enter Lidarr API Key: ")
users = None  # List of users to sync to (Defaults to log in user, additional users must be hardcoded)
# users MUST be in a list, i.e. ["user1"], even if its a single user. "user1", user1, etc are not valid
"""
#Switch to this block if you want to hardcode your keys and URLs
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
keepgoing = False #Used later for loop
lidarrimport = False
PLEX_SERVER_TOKEN = ""
PLEX_SERVER_URL = ""
LIDARR_IP = ""
LIDARR_TOKEN = ""
users = None
"""

session = requests.Session()  # Open session
session.verify = False  # Ignore SSL errors
plex = PlexServer(
    PLEX_SERVER_URL, PLEX_SERVER_TOKEN, session=session
)  # Connect to Plex server
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
    )
)  # Connect to Spotify API


def extract_playlist_id(playlist_url):  # parse playlist ID from URL if applicable
    if "playlist/" in playlist_url:
        playlist_id = playlist_url.split("playlist/")[
            1
        ]  # Remove excess text if inputting URL manually and not via Lidarr
        return playlist_id
    else:
        playlist_id = playlist_url
        return playlist_id


def get_spotify_playlist_tracks(
    playlist_id,
):  # Get all tracks from Spotify, check Plex to see if they exist, and then add them to a list for Plex to use in create_list
    try:
        results = sp.playlist_tracks(playlist_id)
        music = plex.library.section(
            "Music"
        )  # Set music as active library and assign it to music variable
        plex_tracks = []
        while results:
            for item in results["items"]:
                try:
                    track_name = item["track"]["name"]
                    artist_name = item["track"]["artists"][0]["name"]
                    for track in music.search(
                        title=artist_name
                    ):  # search for the artist in plex
                        try:
                            plex_tracks.append(
                                track.track(title=track_name)
                            )  # See if the artist has a track in plex that matches the song name
                        except:
                            continue
                except Exception as x2:
                    print(
                        "Something went wrong with Playlist ID "
                        + playlist_id
                        + " and track "
                        + track_name
                    )
                    print("Error is as follows: ")
                    print(x2)
                    continue
            if results["next"]:
                results = sp.next(results)
            else:
                break
        return plex_tracks
    except Exception as x:
        print("Error reported, probably a 404. See documentation for more info.")
        print("Error is as follows: ")
        print(x)


def getplaylistname(
    playlist_id,
):  # Get the name of the playlist so create_list can use it
    try:
        playlistname = sp.playlist(playlist_id, fields=["name"])
        playlist_name = playlistname["name"]
        return playlist_name
    except Exception as x3:
        print(
            "I've never seen this occur without also getting a 404 on the previous block, please submit a bug report if this is inaccurate"
        )
        print(x3)


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


def create_list(plexuser, plextracks, playlist_name):
    plexplaylist_id = None  # init playlistid variable
    plexconn = plexuser  # replaces old plexconn variable which was just default user before, now it will take each user as needed
    # Get a list of existing playlists from Plex
    for (
        playlist
    ) in (
        plexconn.playlists()
    ):  # Checks each playlist to see if the playlist exists via name
        if playlist_name in playlist.title:
            plexplaylist_id = playlist.ratingKey
            break

    if plexplaylist_id is not None:  # If playlist exists
        try:
            print("Playlist found, matching and updating:" + playlist_name)
            plexconn.fetchItem(plexplaylist_id).addItems(plextracks)
            print("Playlist '" + playlist_name + "' synchronized with Spotify")
            return plexplaylist_id
        except Exception as x3:
            print(
                "Playlist"
                + playlist_name
                + "appears to match existing, but we ran into an issue while updating."
            )
            print(x3)
            pass
    else:  # If playlist is new/doesn't exist
        try:
            plex_playlist = plexconn.createPlaylist(
                title=playlist_name, items=plextracks
            )
            if plex_playlist:
                print(f"Playlist '{playlist_name}' created successfully on Plex.")
            else:
                print("Failed to create the playlist.")
                return 0
        except:
            print("Creation failed, are there tracks in your playlist?")
            # This shouldn't occur (as a fault of this script) if you have tracks. If you see this, please submit a bug report
            pass


mode = input(
    "Do you want to import a playlist directly(1), or use a Lidarr Import List(2)? "
)
print(
    "If you want to copy playlists to other users as well, enter their names in the users variable at the top of the script"
)

if mode != "1" and mode != "2":  # catches invalid input
    print("Sorry, " + mode + " is not a valid option!")
elif mode == "1":  # sets keepgoing to true until next manual import loop
    keepgoing = True
elif mode == "2":  # jumps to lidarrimport loop
    lidarrimport = True


if lidarrimport == True:
    print("Importing from Lidarr instance at: " + LIDARR_IP)
    try:
        playlists = getlidarrlists()  # grab all spotify playlist in import sync
        print(
            playlists
        )  # print all playlist ID's to console, I might make this print playlist names at some point
        for playlist in playlists:
            try:
                print(playlist)  # current playlist being synced
                PLAYLIST_url = playlist
                PLAYLIST_ID = extract_playlist_id(PLAYLIST_url)
                get_tracks = get_spotify_playlist_tracks(PLAYLIST_ID)
                get_name = getplaylistname(PLAYLIST_ID)
                plexplaylist_id = create_list(plex, get_tracks, get_name)
                if users != None:
                    for user in users:
                        altuser = plex.switchUser(user)
                        print("Creating for ", user)
                        PLAYLIST_url = playlist
                        PLAYLIST_ID = extract_playlist_id(PLAYLIST_url)
                        get_tracks = get_spotify_playlist_tracks(PLAYLIST_ID)
                        get_name = getplaylistname(PLAYLIST_ID)
                        plexplaylist_id = create_list(altuser, get_tracks, get_name)
                else:
                    continue
            except Exception as error3:
                print("Error:")
                print(error3)

    except Exception as errormsg:
        print(
            "Failure, most likely one of your variables is wrong, or your Spotify playlist is not compatible, see documentation"
        )
        print(errormsg)


while keepgoing == True:  # manual import loop
    try:
        PLAYLIST_url = input("Playlist ID or url: ")  # input for playlist ID
        PLAYLIST_ID = extract_playlist_id(PLAYLIST_url)
        get_tracks = get_spotify_playlist_tracks(PLAYLIST_ID)
        get_name = getplaylistname(PLAYLIST_ID)
        create_list(get_tracks, get_name)
        asker = input("Keep adding? Y/N: ")
        if asker != "Y" and asker != "y":
            keepgoing = False
        else:
            keepgoing = True
    except:
        print(
            "Failure, most likely one of your variables is wrong, or your Spotify playlist is not compatible, see documentation"
        )
else:
    exit()
