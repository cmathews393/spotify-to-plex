from pathlib import Path

import rtoml
from loguru import logger

config_file = Path("config.toml")
env_file = Path("spotiplex.env")


def ensure_config_exists() -> None:
    """Ensure the configuration file exists, and create it with default values if it doesn't."""
    if not Path.exists(config_file):
        logger.warning("config file missing!")
        logger.debug("Current Working Directory:", Path.cwd())
        with Path.open(config_file) as file:
            rtoml.dump({}, file)


def read_config(service: str) -> dict[str, str]:
    """Read config for a given service."""
    logger.debug("Reading config...")
    ensure_config_exists()  # Check if config file exists
    with Path.open(config_file) as file:
        config = rtoml.load(file)
    return config.get(service, {})


def write_config(service: str, data):
    """Write config for a given service (not in use)."""
    print("writing config")
    ensure_config_exists()  # Check if config file exists
    with open(config_file) as file:
        config = rtoml.load(file)
    config[service] = data
    with open(config_file, "w") as file:
        rtoml.dump(config, file)


def config_to_env() -> None:
    """Convert the config.toml to an env file."""
    logger.debug("Converting config.toml to .env file...")
    ensure_config_exists()
    with Path.open(config_file) as file:
        config = rtoml.load(file)

    with open(env_file, "w") as env:
        # Write Spotify config
        spotify_config = config.get("spotify", {})
        env.write(f"SPOTIFY_API_KEY={spotify_config.get('api_key', '')}\n")
        env.write(f"SPOTIFY_API_ID={spotify_config.get('client_id', '')}\n")

        # Write Plex config
        plex_config = config.get("plex", {})
        env.write(f"PLEX_API_KEY={plex_config.get('api_key', '')}\n")
        env.write(f"PLEX_SERVER_URL={plex_config.get('url', '')}\n")
        env.write(f"PLEX_REPLACE={plex_config.get('replace', '')}\n")

        # Write Lidarr config
        lidarr_config = config.get("lidarr", {})
        env.write(f"LIDARR_API_KEY={lidarr_config.get('api_key', '')}\n")
        env.write(f"LIDARR_API_URL={lidarr_config.get('url', '')}\n")

        # Write Spotiplex config
        spotiplex_config = config.get("spotiplex", {})
        env.write(f"PLEX_USERS={spotiplex_config.get('plex_users', '')}\n")
        env.write(f"WORKER_COUNT={spotiplex_config.get('worker_count', 10)}\n")
        env.write(f"SECONDS_INTERVAL={spotiplex_config.get('seconds_interval', 60)}\n")
        env.write(
            f"MANUAL_PLAYLISTS={spotiplex_config.get('manual_playlists', 'None')}\n",
        )
        env.write(f"LIDARR_SYNC={spotiplex_config.get('lidarr_sync', 'false')}\n")
        env.write(f"FIRST_RUN={spotiplex_config.get('first_run', 'False')}\n")

    logger.debug(".env file created successfully.")
