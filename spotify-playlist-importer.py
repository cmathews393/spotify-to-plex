import plexapi
from plexapi.server import PlexServer
import requests 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Plex API hates SSL or something idk it was annoying

SPOTIPY_CLIENT_ID = input('Spotify Client ID: ') 
SPOTIPY_CLIENT_SECRET = input('Spotify Secret: ')
keepgoing = False #Used later for loop
lidarrimport = False
PLEX_SERVER_TOKEN = input('PLEX Server Token: ') 
PLEX_SERVER_URL = input('Server URL, include http(s) and port, eg https://192.168.1.2:32400: ')
LIDARR_IP = input('If desired, enter Lidarr IP, include HTTP and port number: ')
LIDARR_TOKEN = input('If desired, enter Lidarr API Key: ')

'''
#Switch to this block if you want to hardcode your keys and URLs
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
keepgoing = False #Used later for loop
lidarrimport = False
PLEX_SERVER_TOKEN = ""
PLEX_SERVER_URL = ""
LIDARR_IP = ""
LIDARR_TOKEN = ""
'''

session = requests.Session() #Open session
session.verify = False #Ignore SSL errors
plex = PlexServer(PLEX_SERVER_URL, PLEX_SERVER_TOKEN, session=session) #Connect to Plex server
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)) #Connect to Spotify API

def extract_playlist_id(playlist_url): #parse playlist ID from URL if applicable
    if "playlist/" in playlist_url:
        playlist_id = playlist_url.split("playlist/")[1]
        return playlist_id
    else:
        playlist_id = playlist_url
        return playlist_id

def get_spotify_playlist_tracks(playlist_id): #Get all tracks from Spotify, check Plex to see if they exist, and then add them to a list for Plex to use in create_list
    try:
        results = sp.playlist_tracks(playlist_id)
        music = plex.library.section('Music')
        plex_tracks = []
        while results:
            for item in results['items']:
                try:
                    track_name = item['track']['name']
                    artist_name = item['track']['artists'][0]['name']
                    for track in music.search(title=artist_name):
                        try:
                            plex_tracks.append(track.track(title=track_name))
                        except:
                            continue
                except Exception as x2:
                    print("Something went wrong with Playlist ID "+playlist_id+" and track "+track_name)
                    print("Error is as follows: ")
                    print(x2)
                    continue         
            if results['next']:
                results = sp.next(results)
            else:
                break
        return plex_tracks
    except Exception as x:
        print("Error reported, probably a 404. See documentation for more info.")
        print("Error is as follows: ")
        print(x)
    

def getplaylistname(playlist_id): #Get the name of the playlist so create_list can use it
    try:
        
        playlistname = sp.playlist(playlist_id, fields=["name"])
        playlist_name = playlistname["name"]
        return playlist_name
    except Exception as x3:
        print("I'm tired of writing error messages, see above.")
        print(x3)


def make_lidarr_api_call(api_key, endpoint, params=None):

    headers = {
        "X-Api-Key": api_key,
    }

    url = f"{LIDARR_IP}{endpoint}"
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
def getlidarrlists():
    api_key = LIDARR_TOKEN  # Replace with your actual Lidarr API key
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

def create_list(plextracks,playlist_name):
    
    try:
        plex_playlist = plex.createPlaylist(title=playlist_name, items=plextracks)
        if plex_playlist:
            print(f"Playlist '{playlist_name}' created successfully on Plex.")
        else:
            print("Failed to create the playlist.")
            return(0)
    except:
        print("Creation failed, are there tracks in your playlist?")
        pass
    #pms.createPlaylist(title="testing")
        #if plex_playlist:
        #    print(f"Playlist '{playlist_name}' created successfully on Plex.")
        #else:
         #   print("Failed to create the playlist.")
         #   return(0)

mode = input("Do you want to import a playlist directly(1), or use a Lidarr Import List(2)? ")

if mode != "1" and mode != "2":
    print("Sorry, "+mode+" is not a valid option!")
elif mode == "1":
    keepgoing = True
elif mode == "2":
    lidarrimport = True


if lidarrimport == True:
    print("Importing from Lidarr instance at: "+LIDARR_IP)
    try:
        playlists = getlidarrlists()
        print(playlists)
        for playlist in playlists:
            print(playlist)
            PLAYLIST_url = playlist
            PLAYLIST_ID = extract_playlist_id(PLAYLIST_url)
            get_tracks = get_spotify_playlist_tracks(PLAYLIST_ID)
            get_name = getplaylistname(PLAYLIST_ID)
            create_list(get_tracks,get_name)
        
    except:
        print("Failure, most likely one of your variables is wrong, or your Spotify playlist is not compatible")    



while keepgoing == True:
    try:
        PLAYLIST_url = input('Playlist ID or url: ')
        PLAYLIST_ID = extract_playlist_id(PLAYLIST_url)
        get_tracks = get_spotify_playlist_tracks(PLAYLIST_ID)
        get_name = getplaylistname(PLAYLIST_ID)
        create_list(get_tracks,get_name)
        asker = input("Keep adding? Y/N: ")
        if asker != "Y" and asker != "y":
            keepgoing = False
        else:
            keepgoing = True
    except:
        print("Failure, most likely one of your variables is wrong, or your Spotify playlist is not compatible")    
else:
    exit()
