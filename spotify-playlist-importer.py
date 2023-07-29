import plexapi
from plexapi.server import PlexServer
import requests 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Plex API hates SSL or something idk it was annoying

SPOTIPY_CLIENT_ID = input('Spotify Client ID: ') 
SPOTIPY_CLIENT_SECRET = input('Spotify Secret: ')
keepgoing = True #Used later for loop
PLEX_SERVER_TOKEN = input('PLEX Server Token: ') 
PLEX_SERVER_URL = input('Server URL, include http(s) and port, eg https://192.168.1.2:32400: ')

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
    results = sp.playlist_tracks(playlist_id)
    music = plex.library.section('Music')
    plex_tracks = []
    while results:
        for item in results['items']:
            track_name = item['track']['name']
            artist_name = item['track']['artists'][0]['name']
            for track in music.search(title=artist_name):
                try:
                    plex_tracks.append(track.track(title=track_name))
                except:
                    pass
                    
        if results['next']:
            results = sp.next(results)
        else:
            break
    return plex_tracks

def getplaylistname(playlist_id): #Get the name of the playlist so create_list can use it

    playlistname = sp.playlist(playlist_id, fields=["name"])
    playlist_name = playlistname["name"]
    return playlist_name
    
def create_list(plextracks,playlist_name):
    plex_playlist = plex.createPlaylist(title=playlist_name, items=plextracks)
    #pms.createPlaylist(title="testing")
    if plex_playlist:
        print(f"Playlist '{playlist_name}' created successfully on Plex.")
    else:
        print("Failed to create the playlist.")
        return(0)

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
