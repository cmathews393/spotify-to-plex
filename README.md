# Spotify To Plex 

Spotify To Plex is a simple Python script to import Spotify Playlists by ID or URL into Plex, automatically finding tracks in the playlist that are in your Plex library. It can import tracks from your Spotify playlists that are synced down to Lidarr, which you can use to automatically sort and rename music files that you have the legal right to distribute and/or maintain copies of. 

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

Disclaimer: I am not responsible for how you utilize this script, nor am I responsible for your usage of the Spotify API, in or outside of conjuction with this script. Please read the Spotify TOS and Spotify Developer TOS carefully. I am not, and have never been associated with or employed by Spotify, and this script is neither endorsed nor supported by Spotify. All uses of this script are at your own risk. Please buy the music you enjoy. 
