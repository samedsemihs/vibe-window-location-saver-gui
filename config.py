"""Configuration management for Screen Location Saver."""

import json
import os
import sys

CONFIG_FILE = "config.json"

_defaults = {
    "language": "tr",
}


def _config_path():
    """Get path to config file (next to exe or source)."""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, CONFIG_FILE)


def load_config() -> dict:
    """Load configuration from file, return defaults if not found."""
    path = _config_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Merge with defaults
                return {**_defaults, **data}
        except (json.JSONDecodeError, IOError):
            pass
    return _defaults.copy()


def save_config(config: dict):
    """Save configuration to file."""
    path = _config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get(key: str, default=None):
    """Get a config value."""
    config = load_config()
    return config.get(key, default)


def set(key: str, value):
    """Set a config value and save."""
    config = load_config()
    config[key] = value
    save_config(config)
