# SPDX-FileCopyrightText: 2023-present László Szurok <48314396+laszloszurok@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

import os
import sys
import time
from datetime import datetime

import dbus
import schedule

from tvnotipy.config import getters
from tvnotipy.config.constants import Config
from tvnotipy.utils import helpers


def main() -> None:
    cache_dir = getters.get_cache_dir()

    if len(series_list := getters.get_series_list()) == 0:
        print("No urls found.")
        print(f"The file {Config.CONFIG_DIR}/urls should contain a list of Wikpedia urls for TV series, one per line.")
        sys.exit(1)

    schedule.every().day.do(helpers.check_new_seasons, series_list, cache_dir)

    while True:
        schedule.run_pending()

        for series in series_list:
            cache_file = series["cache_file"]
            if os.path.isfile(cache_file):
                if ((datetime.now().timestamp() - os.path.getmtime(cache_file)) / (60 * 60 * 24)) < 2:
                    title = str(cache_file).split("/")[-1]
                    obj = dbus.SessionBus().get_object(
                        "org.freedesktop.Notifications", "/org/freedesktop/Notifications"
                    )
                    interface = dbus.Interface(obj, "org.freedesktop.Notifications")
                    interface.Notify("", 0, "", "New season", f"{title}", [], {"urgency": 1}, 10000)

        time.sleep(7200)
