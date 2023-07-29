# Spotify To Plex 

Spotify To Plex is a simple Python script to import Spotify Playlists by ID or URL into Plex, automatically finding tracks in the playlist that are in your Plex library. 

Currently you need 4 things (5 if you count the playlist): A Spotify Client ID, a Spotify Client Secret, a Plex Server Token, and your Plex Server URL. 

Some limitations right now are:
1). Single playlist import at a time
2). Recreates the playlist everytime the script is run, rather than updating it
3). Initially, didn't let you loop back, but I think that's fixed. 

Currently, working on an update that will allow you to pull playlists from Lidarr Import lists. That's more useful to me, but I will add some sort of list functionality eventually, maybe ability to import a csv?
Working on fixing the playlist recreation issue as well. Will also maybe add a GUI eventually, but GUIs are a pain in the ass. 

Using https://github.com/pkkid/python-plexapi, https://github.com/spotipy-dev/spotipy, and the requests library. 
