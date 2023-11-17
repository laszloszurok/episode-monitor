import logging
import sys
import textwrap
import time

from tvnotipy.config import getters
from tvnotipy.config.constants import EnvPath
from tvnotipy.utils import helpers


def main() -> None:
    cache_dir = getters.get_cache_dir()
    series_list = getters.get_series_list()

    if len(series_list) == 0:
        msg = f"""
        No urls found: {EnvPath.CONFIG_DIR}/urls
        The file should contain a list of Wikpedia urls for TV series, one per line.
        """
        logging.error(textwrap.dedent(msg))
        sys.exit(1)

    while True:
        helpers.new_season_notify(series_list=series_list, cache_dir=cache_dir)

        time.sleep(7200)
