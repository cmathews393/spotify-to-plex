from plexapi.server import PlexServer
import requests
import urllib3 
from confighandler import read_config


class PlexConnector:
    def __init__(self):
        self.config = read_config('plex')  # Call read_config directly
        self.session = self.create_session()

    def create_session(self):
        session = requests.Session()
        session.verify = False  # Ignore SSL errors
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        return session

    def connect_plex(self):
        url, token = self.plexconfig()
        return PlexServer(url, token, session=self.session)

    def plexconfig(self):
        url = self.config.get('url')
        token = self.config.get('api_key')
        return url, token

