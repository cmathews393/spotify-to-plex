"""Init for Typer app/main functions."""

import sys

import typer
from loguru import logger

import spotiplex.modules.confighandler.main as config_handler
import spotiplex.modules.spotiplex.main as sp_module
from spotiplex.config import Config

logger.trace("Initializing logger...")
logger.remove()
logger.add("spotiplex.log", rotation="12:00")
logger.debug("Spotiplex v126")

logger.trace("Initializing app...")
app = typer.Typer()


@app.command()
def sync_lidarr_imports() -> None:
    """Syncs all playlists currently being pulled via Lidarr."""
    logger.debug("We are running on commit: ", Config.SPOTIPLEX_VERSION)
    sp_instance = sp_module.Spotiplex(lidarr=True, playlist_id=None)
    sp_instance.run()


@app.command()
def generate_env() -> None:
    """Generate env file from config to use with docker."""
    logger.add(sys.stdout)
    config_handler.config_to_env()


@app.command()
def sync_manual_lists() -> None:
    """Syncs all playlists specified in config file."""
    logger.debug("We are running on commit: ", Config.SPOTIPLEX_VERSION)
    sp_instance = sp_module.Spotiplex(lidarr=False, playlist_id=None)
    sp_instance.run()


# Uncomment and complete this function if needed in the future
# @app.command()
# def sync_single_list(playlist_id: str) -> None:
#     """Takes a playlist URL or ID and manually syncs."""
#     sp_instance = sp_module.Spotiplex()
#     sp_instance.sync_single_playlist(playlist_id)
# TODO(@cmathews393): Testing todo generation
if __name__ == "__main__":
    app()
