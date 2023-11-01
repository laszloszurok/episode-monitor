import logging
import os
import sys
import textwrap
import time

import schedule

from tvnotipy.config import getters
from tvnotipy.config.constants import EnvPath
from tvnotipy.utils import helpers


def main() -> None:
    cache_dir = getters.get_cache_dir()

    if len(series_list := getters.get_series_list()) == 0:
        msg = f"""
        No urls found: {EnvPath.CONFIG_DIR}/urls
        The file should contain a list of Wikpedia urls for TV series, one per line.
        """
        logging.error(textwrap.dedent(msg))
        sys.exit(1)

    schedule.every().day.do(helpers.check_new_seasons, series_list, cache_dir)

    while True:
        schedule.run_pending()

        for series in series_list:
            cache_file = series["cache_file"]
            if os.path.isfile(cache_file):
                if helpers.is_modified_lately(cache_file):
                    helpers.send_desktop_notification(title="New season", message=str(cache_file).split("/")[-1])

        time.sleep(7200)
