# Spotify To Plex (Spotiplex)
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C2PUDV8)

- [Spotify To Plex (Spotiplex)](#spotify-to-plex-spotiplex)
- [How To](#how-to)
- [Latest Features:](#latest-features)
- [Dependencies](#dependencies)
- [Upcoming Planned Features](#upcoming-planned-features)
- [Known Issues:](#known-issues)
- [Disclaimer:](#disclaimer)


# <h3>How To</h3>

<h2>Prerequisites</h2>
1). Ensure you have Python 3 installed. Spotiplex is developed on 3.8.10, but may work on different versions, though this is unsupported.
<br>
2). Install plexapi, spotipy, and python-decouple ("pip install python-decouple plexapi spotipy")

<h2> Setup (Script version)</h2>
1). Clone the repo
<br>
2). Rename default.env to .env
<br>
3). Configure settings for your environment
<br>
    a). Get Plex API key
    <br>
    b). Get Spotify ID and API key
    <br>
    c). Get Lidarr API key
    <br>
4). Run "main.py" from the "current-version" folder

<h2> Setup (Docker Version)</h2>
Note: I've only tested on Linux, Docker version 24.0.5, build 24.0.5-0ubuntu1~22.04.1. Anything else is "unsupported" I guess, but if you have issues let me know, especially on Docker Desktop for Windows. I can't reliably test because I don't want to upgrade to Win11, but I can spin up a VM if needed

1). `docker pull 0xchloe/spotiplex`  
2). `touch spotiplex.env`  
3). Copy the contents of default.env from this repo to your new .env file, and edit as needed  
4). `docker run --env-file spotiplex.env 0xchloe/spotiplex`  
5). Re-start container to re-sync. For obvious reasons, manual input is not supported for the container, so if you need to manually input playlist ID's and for whatever reason can't use your env, clone the repo instead  



# <h4>Latest Features:</h4>

Multithreading added in the latest update! Previously an import from Lidarr with approx 35-45 playlists would take an hour or more. Multithreading cuts this down to 10 minutes or less in most cases. Working on an all-in-one binary as well. Creds and variables are available in an .env. The default.env provides 

Primarily, this app has been redesigned around using Lidarr as the source for playlists to sync.

Spotiplex is a simple Python app to import Spotify Playlists by ID or URL into Plex, automatically finding tracks in the playlist that are in your Plex library. It can import tracks from your Spotify playlists that are synced down to Lidarr, which you can use to automatically sort and rename music files that you have the legal right to distribute and/or maintain copies of. 

# <h4>Dependencies</h4>
Using https://github.com/pkkid/python-plexapi, https://github.com/spotipy-dev/spotipy, and the requests library. 

# <h3>Upcoming Planned Features</h3>

See the <a href=https://trello.com/b/PGhCi2Ws/spotiplex-roadmap>Trello Board</a> for more details

<br>
1). Packaging an exe for easier Windows deployments
<br>
2). Webapp deployment option
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
