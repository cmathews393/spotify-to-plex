# Spotify To Plex (Spotiplex)

## Table of Contents

- [How To](#how-to)
- [Dependencies](#dependencies)
- [Upcoming Planned Features](#upcoming-planned-features)
- [Known Issues](#known-issues)
- [Disclaimer](#disclaimer)

**Note:** Temporarily change-frozen (except for all the times I've updated this instead of working on Playlist Manager), building a new app that implements similar functionality for Radarr, Sonarr, etc, using Trakt and IMDB lists or *arr tags. Will be implemented with a web interface from the start, so is naturally taking a bit more time. [New app repo is here](https://github.com/cmathews393/plex-playlist-manager).

## How To

### Prerequisites

1. Ensure you have Python 3 installed (if not running docker)
2. Ensure you have poetry installed
3. Ensure you have a Spotify api key [from here](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)

### Setup (Script Version)

1. Clone the repo.
2. Configure settings for your environment:
   - Get Plex API key.
   - Get Spotify ID and API key.
   - Get Lidarr API key.
3. Run with poetry (`cd spotiplex && poetry install`, `poetry run spotiplex --help`)
4. Follow CLI prompts

### Setup (Docker Version)

Note: Tested only on Linux, Docker version 24.0.5. Other environments are "unsupported", but issues can be reported.

1. `docker pull 0xchloe/spotiplex:latest`
2. `touch spotiplex.env`
3. Copy the contents of `default.env` from this repo to your new `.env` file, and edit as needed.
4. `docker run --env-file spotiplex.env 0xchloe/spotiplex`
5. Container will run sync of Lidarr lists and manually specified lists on initial start, and every day at midnight if CRON_SCHEDULE is not set

## Dependencies

Using [python-plexapi](https://github.com/pkkid/python-plexapi), [spotipy](https://github.com/spotipy-dev/spotipy), [rtoml](https://github.com/samuelcolvin/rtoml), typer, supercronic, httpx

## Upcoming Planned Features

- Add to Plex-Playlist-Manager (See above)

## Known Issues

1. Some Spotify Playlists, especially auto-generated and non-public ones, may not be accessible via API, resulting in 404 errors.
2. Occasional track errors in certain playlists. The script will continue and import the rest of the playlist, noting any issues.

## Disclaimer

I am not responsible for how you utilize this script, nor am I responsible for your usage of the Spotify API, in or outside of conjunction with this script. Please read the Spotify TOS and Spotify Developer TOS carefully. This script is neither endorsed nor supported by Spotify. All uses of this script are at your own risk. Please buy the music you enjoy.
