# Spotify To Plex 

Spotify To Plex is a simple Python script to import Spotify Playlists by ID or URL into Plex, automatically finding tracks in the playlist that are in your Plex library. 

Currently you need 4 things (5 if you count the playlist): A Spotify Client ID, a Spotify Client Secret, a Plex Server Token, and your Plex Server URL. 


Using https://github.com/pkkid/python-plexapi, https://github.com/spotipy-dev/spotipy, and the requests library. 

<h3>Upcoming Planned Features</h3>
<br>
1). Stored creds in a config file or env
<br>
2). Packaging an exe for easier Windows deployments
<br>
3). GUI (long-term)

<h3>Known Issues:</h3>
<br>
1). Some Spotify Playlists don't appear to be accessible via API. Specifically, auto-generated playlists that are not public I believe. I don't think there's a way around this, but if it appears in a list, and you get a 404 error, that's what's happening. If you figure out a way to make it import, submit a pull request and I'd be happy to merge it. 
<br>
<br>
2). Some tracks error out on certain playlists. Unsure why, but the script should continue and import the rest of the playlist, and let you know which playlist + song had issues. Usually only one song per list, so very low priority. 


