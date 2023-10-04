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
    return PlexServer(PLEX_SERVER_URL, PLEX_SERVER_TOKEN, session=session)


def connect_spotify():
    SPOTIPY_CLIENT_ID = config("SPOTIFY_API_ID")
    SPOTIPY_CLIENT_SECRET = config("SPOTIFY_API_KEY")
    return spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
        )
    )


def extract_playlist_id(playlist_url):  # parse playlist ID from URL if applicable
    return (
        playlist_url.split("playlist/")[1]
        if "playlist/" in playlist_url
        else playlist_url
    )


def get_spotify_tracks(sp, playlist_id):
    try:
        results = sp.playlist_tracks(playlist_id)
    except Exception as exception1:
        name = get_playlist_name(sp, playlist_id)
        print(f"Error getting tracks for playlist {name}, playlistID: {playlist_id}")
        print(exception1)
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
        # print(f"Track: {track_name}, Artist: {artist_name}")
        if artist_tracks_in_plex := music.search(title=artist_name):
            try:
                for track in artist_tracks_in_plex:
                    if plex_track := track.track(title=track_name):
                        plex_tracks.append(plex_track)
                        # print(track_name, " by ", artist_name, " appended to list")
                        orig_tracks.append([track_name, artist_name])
                    else:
                        orig_tracks.append([track_name, "Song Not in Plex"])
            except Exception as e:
                # print(
                #     track_name, " by ", artist_name, " not found, usually missing track"
                # )
                orig_tracks.append([track_name, "Song Not in Plex"])
        else:
            # print(
            #     track_name, " by ", artist_name, " not found, usually missing artist. "
            # )
            continue

    return plex_tracks, orig_tracks


def get_playlist_name(sp, playlist_id):
    """Retrieve the name of the playlist for further use in create_list."""
    try:
        playlist_data = sp.playlist(playlist_id, fields=["name"])
        print(playlist_data["name"], " is being processed")
        return playlist_data["name"]
    except Exception as e:
        print(
            "Error retrieving playlist name. If this is unexpected, please submit a bug report."
        )
        print(e)


def make_lidarr_api_call(params=None):
    LIDARR_IP = config("LIDARR_IP")
    LIDARR_TOKEN = config("LIDARR_TOKEN")
    LIDARR_ENDPOINT = config("LIDARR_ENDPOINT", default="/api/v1/importlist")
    # Add API key to header
    headers = {
        "X-Api-Key": LIDARR_TOKEN,
    }
    # Combine lidarr IP with API call
    url = f"{LIDARR_IP}{LIDARR_ENDPOINT}"

    # Store response from Lidarr
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    print(f"Error: {response.status_code} - {response.text}")
    return None


def getlidarrlists():
    # This shouldn't change, but if it does and it stops working for you, submit a bug report and I'll fix
    if result := make_lidarr_api_call():
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
    plexconn = plexuser
    plexplaylist_id = next(
        (
            playlist.ratingKey
            for playlist in plexconn.playlists()
            if playlist_name in playlist.title
        ),
        None,
    )

    if plexplaylist_id:  # If playlist exists
        print(f"Playlist found, matching and updating: {playlist_name}")
        try:
            plexconn.fetchItem(plexplaylist_id).addItems(plextracks)
            # print(f"Playlist '{playlist_name}' synchronized with Spotify")
            return plexplaylist_id
        except Exception as e:
            print(
                f"Playlist {playlist_name} appears to match existing, but an issue occurred while updating."
            )
            print(e)

    else:  # If playlist doesn't exist
        try:
            plex_playlist = plexconn.createPlaylist(
                title=playlist_name, items=plextracks
            )
            if plex_playlist:
                print(f"Playlist '{playlist_name}' created successfully on Plex.")
            else:
                print("Failed to create the playlist.")
                return 0
        except Exception:
            print("Creation failed. Ensure there are tracks in your playlist.")


def lidarr_import(LIDARR_IP, playlist, plex, users):
    print(f"Importing from Lidarr instance at: {LIDARR_IP}")

    try:
        playlists = getlidarrlists()
        # Consider enhancing the 'getlidarrlists' function to return playlist names too,
        # then you can print those names directly instead of just IDs.
        print(playlists)

        for playlist in playlists:
            try:
                print(playlist)
                PLAYLIST_ID = extract_playlist_id(playlist)
                tracks = get_spotify_playlist_tracks(PLAYLIST_ID)
                name = get_playlist_name(PLAYLIST_ID)

                create_list(plex, tracks, name)

                if users:
                    for user in users:
                        altuser = plex.switchUser(user)
                        print(f"Creating for {user}")
                        create_list(altuser, tracks, name)

            except Exception as error3:
                print("Error encountered during playlist processing:")
                print(error3)

    except Exception as errormsg:
        print(
            "Failure, most likely due to incorrect variables or incompatible Spotify playlist. Refer to documentation."
        )
        print(errormsg)


def process_playlist(playlist, plex, sp):
    try:
        playlist_id = extract_playlist_id(playlist)
        playlist_name = get_playlist_name(sp, playlist_id)
        spotify_tracks = get_spotify_playlist_tracks(sp, playlist_id)
        plex_tracks, _ = check_tracks_in_plex(plex, spotify_tracks)
        create_list(plex, plex_tracks, playlist_name)
        print(f"Processed playlist '{playlist_name}'.")
    except Exception as e:
        print(f"Error processing playlist '{playlist}':", e)
