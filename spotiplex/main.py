from plex import PlexConnector as pc
from confighandler import ensure_config_exists, read_config
from spotify import SpotifyConnector as sc


plexconnection= pc.connect_plex()
spotifyconnection = sc.connect_spotify()
lidarrconnection = lc.connect_lidarr()