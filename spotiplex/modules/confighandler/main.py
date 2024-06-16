import os
from pathlib import Path

import rtoml
from loguru import logger

config_file = Path("config.toml")


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
