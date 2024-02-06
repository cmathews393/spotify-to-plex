import rtoml
import os

config_file = "config.toml"


def ensure_config_exists():
    """Ensure the configuration file exists, and create it with default values if it doesn't."""
    if not os.path.exists(config_file):
        print("config file missing!")
        print("Current Working Directory:", os.getcwd())
        with open(config_file, "w") as file:
            rtoml.dump({}, file)


def read_config(service):
    print("reading config")
    ensure_config_exists()  # Check if config file exists
    with open(config_file, "r") as file:
        config = rtoml.load(file)
    return config.get(service, {})


def write_config(service, data):
    print("writing config")
    ensure_config_exists()  # Check if config file exists
    with open(config_file, "r") as file:
        config = rtoml.load(file)
    config[service] = data
    with open(config_file, "w") as file:
        rtoml.dump(config, file)
