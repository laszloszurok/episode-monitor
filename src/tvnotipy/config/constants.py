import os
from pathlib import Path


class EnvPath:
    CACHE_DIR = (
        f"{xdg_cache}/tvnotipy"
        if (xdg_cache := os.getenv("XDG_CACHE_HOME")) and os.path.isabs(xdg_cache)
        else Path.home().joinpath(".cache", "tvnotipy")
    )

    CONFIG_DIR = (
        f"{xdg_config}/tvnotipy"
        if (xdg_config := os.getenv("XDG_CONFIG_HOME")) and os.path.isabs(xdg_config)
        else Path.home().joinpath(".config", "tvnotipy")
    )

    URLS_FILE = os.path.join(CONFIG_DIR, "urls")
