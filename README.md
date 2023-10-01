# Spotify To Plex (Spotiplex)


- [Spotify To Plex (Spotiplex)](#spotify-to-plex-spotiplex)
- [Latest Features:](#latest-features)
- [Dependencies](#dependencies)
- [Upcoming Planned Features](#upcoming-planned-features)
- [Known Issues:](#known-issues)
- [Disclaimer:](#disclaimer)

# <h4>Latest Features:</h4>

Multithreading added in the latest update! Previously an import from Lidarr with approx 35-45 playlists would take an hour or more. Multithreading cuts this down to 10 minutes or less in most cases. The per user sync is not implemented in the new build, but should be implemented in the next update or so. Working on an all-in-one binary as well. Creds and variables are available in an .env. The default.env provides 

Primarily, this app has been redesigned around using Lidarr as the source for playlists to sync.

Spotiplex is a simple Python app to import Spotify Playlists by ID or URL into Plex, automatically finding tracks in the playlist that are in your Plex library. It can import tracks from your Spotify playlists that are synced down to Lidarr, which you can use to automatically sort and rename music files that you have the legal right to distribute and/or maintain copies of. 

# <h4>Dependencies</h4>
Using https://github.com/pkkid/python-plexapi, https://github.com/spotipy-dev/spotipy, and the requests library. 

# <h3>Upcoming Planned Features</h3>
<br>
1). Re-implement multi-user sync
<br>
2). Packaging an exe for easier Windows deployments
<br>
3). Webapp deployment option
<br>



# <h3>Known Issues:</h3>
<br>
1). Some Spotify Playlists don't appear to be accessible via API. Specifically, auto-generated playlists that are not public I believe. I don't think there's a way around this, but if it appears in a list, and you get a 404 error, that's what's happening. If you figure out a way to make it import, submit a pull request and I'd be happy to merge it. 
<br>
<br>
2). Some tracks error out on certain playlists. Unsure why, but the script should continue and import the rest of the playlist, and let you know which playlist + song had issues. Usually only one song per list, so very low priority. 

<br>
<br>
<br>

# Disclaimer: 
I am not responsible for how you utilize this script, nor am I responsible for your usage of the Spotify API, in or outside of conjuction with this script. Please read the Spotify TOS and Spotify Developer TOS carefully. I am not, and have never been associated with or employed by Spotify, and this script is neither endorsed nor supported by Spotify. All uses of this script are at your own risk. Please buy the music you enjoy. 
