
from plexapi.playlist import Playlist as pl
from plexapi.server import PlexServer
import requests 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib3

def connect_plex(PLEX_SERVER_URL,PLEX_SERVER_TOKEN):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Plex API hates SSL or something idk it was annoying
    session = requests.Session() #Open session
    session.verify = False #Ignore SSL errors
    plex = PlexServer(PLEX_SERVER_URL, PLEX_SERVER_TOKEN, session=session) #Connect to Plex server
    
    return plex

def connect_spotify(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)) #Connect to Spotify API
    return sp

def extract_playlist_id(playlist_url): #parse playlist ID from URL if applicable
    if "playlist/" in playlist_url:
        playlist_id = playlist_url.split("playlist/")[1] #Remove excess text if inputting URL manually and not via Lidarr
        return playlist_id
    else:
        playlist_id = playlist_url
        return playlist_id


def get_spotify_tracks(sp,playlist_id):
    try:
        results = sp.playlist_tracks(playlist_id)
    except:
        print("blerp")
    return results
def check_plex_tracks(spotify_tracks,plex):
    plex_tracks = []
    while spotify_tracks:
        music = plex.library.section('Music')
        for item in spotify_tracks['items']:
            try:
                track_name = item['track']['name']
                artist_name = item['track']['artists'][0]['name']
                if music.search(title=artist_name): #search for the artist in plex
                        for track in music.search(title=artist_name):   
                            if track:
                                try:
                                    plex_track = track.track(title=track_name) #See if the artist has a track in plex that matches the song name
                                    if plex_track:
                                        plex_tracks.append(plex_track)
                                    else:
                                        print("pretend this is an error msg")
                                except Exception:
                                    print("foo2")
            except Exception:
                print("foo")
    return plex_tracks     
def add_plex_tracks():
    print("TODO")
    

def get_spotify_playlist_tracks(sp,plex,playlist_id): #Get all tracks from Spotify, check Plex to see if they exist, and then add them to a list for Plex to use in create_list
    try:
        results = sp.playlist_tracks(playlist_id)
        plex_tracks = []
        display_tracks = []
        while results:
            music = plex.library.section('Music') #Set music as active library and assign it to music variable
            for item in results['items']:
                try:
                    track_name = item['track']['name']
                    artist_name = item['track']['artists'][0]['name']
                    #album_cover = item['track']['image']
                    print(f"Track: {track_name}, Artist: {artist_name}")
                    
                    if music.search(title=artist_name): #search for the artist in plex
                        for track in music.search(title=artist_name):    
                            print("I'm doing this now")    
                            try:
                                print(f"Plex Track: {track_name}")
                                print(f"Artist Name: {artist_name}")
                                if track:
                                    print(f"Matching track_name: {track_name}")
                                    try:
                                        plex_track = track.track(title=track_name) #See if the artist has a track in plex that matches the song name
                                        if plex_track:
                                            plex_tracks.append(plex_track)
                                            display_tracks.append([track_name, artist_name])

                                        else:
                                            print("Artist Error")
                                            plex_tracks.append([track_name, "Artist Missing From Plex"])
                                            display_tracks.append([track_name, "Artist Missing From Plex"])
                                    except Exception as x8:
                                        print(x8)
                                        display_tracks.append([track_name, "Song Not in Plex"])
                                else:
                                    print("No matching artist")
                            except Exception as trackerr:
                                print("oopsie")
                                print(trackerr)
                    else:
                        display_tracks.append(["Artist Not Found","Artist Not Found"]) 
                except Exception as x2:
                    print("Something went wrong with Playlist ID "+playlist_id+" and track "+track_name)
                    print("Error is as follows: ")
                    print(x2)
                    continue

            if results['next']:
                results = sp.next(results)
            else:
                break

        return plex_tracks, results, display_tracks
    except Exception as x:
        print("Error reported, probably a 404. See documentation for more info.")
        print("Error is as follows: ")
        print(x)
    

def getplaylistname(sp,playlist_id): #Get the name of the playlist so create_list can use it
    try:
        
        playlistname = sp.playlist(playlist_id, fields=["name"])
        playlist_name = playlistname["name"]
        return playlist_name
    except Exception as x3:
        print("I've never seen this occur without also getting a 404 on the previous block, please submit a bug report if this is inaccurate")
        print(x3)


def make_lidarr_api_call(LIDARR_IP,api_key, endpoint, params=None):
    #Add API key to header
    headers = {
        "X-Api-Key": api_key,
    }
    #Combine lidarr IP with API call
    url = f"{LIDARR_IP}{endpoint}"
    
    #Store response from Lidarr
    response = requests.get(url, headers=headers, params=params)
    #parse response if it exists, else send error message
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
def getlidarrlists(LIDARR_TOKEN,LIDARR_IP):
    api_key = LIDARR_TOKEN  
    #This shouldn't change, but if it does and it stops working for you, submit a bug report and I'll fix
    endpoint = "/api/v1/importlist"


    result = make_lidarr_api_call(LIDARR_IP,api_key, endpoint)
    if result: #Checks to make sure we got a response
        playlists = [] #initialize playlist... list
        for entry in result: #grabs each playlist
            if entry.get('listType') == 'spotify' and entry.get('fields'): #Check if import list is spotify sourced
                for field in entry['fields']: #search all fields in entry
                    if field.get('name') == 'playlistIds': #Grab playlist ID (i.e. spotify.com/playlist/PLAYLISTID) if the field is playlistid
                        playlists.extend(field.get('value', []))
                        break
        return playlists

def create_list(plexuser,plextracks,playlist_name):
    plexplaylist_id = None #init playlistid variable
    plexconn = plexuser #replaces old plexconn variable which was just default user before, now it will take each user as needed
    # Get a list of existing playlists from Plex
    for playlist in plexconn.playlists(): #Checks each playlist to see if the playlist exists via name 
        if playlist_name in playlist.title:
            plexplaylist_id = playlist.ratingKey
            break
    
    if plexplaylist_id is not None: #If playlist exists
        try:
            print("Playlist found, matching and updating:"+playlist_name)
            plexconn.fetchItem(plexplaylist_id).addItems(plextracks) 
            print("Playlist '"+playlist_name+"' synchronized with Spotify")
            return plexplaylist_id
        except Exception as x3:
            print("Playlist"+playlist_name+"appears to match existing, but we ran into an issue while updating.")
            print(x3)
            pass
    else: #If playlist is new/doesn't exist
        try:
            plex_playlist = plexconn.createPlaylist(title=playlist_name, items=plextracks)
            if plex_playlist:
                print(f"Playlist '{playlist_name}' created successfully on Plex.")
            else:
                print("Failed to create the playlist.")
                return(0)
        except:
            print("Creation failed, are there tracks in your playlist?")
            #This shouldn't occur (as a fault of this script) if you have tracks. If you see this, please submit a bug report
            pass


