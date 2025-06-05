import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".evowood_config.json"

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def set_cloud_credentials(username, password):
    config = load_config()
    config['cloud'] = {'username': username, 'password': password}
    save_config(config)

def get_cloud_credentials():
    config = load_config()
    return config.get('cloud', {})
