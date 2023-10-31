#!/usr/bin/env python

import os
import sys
import time
from datetime import datetime

import config.utils as cu
import dbus
import schedule
import utils.helpers as uh
from config.constants import Config


def main() -> None:
    cache_dir = cu.get_cache_dir()

    if len(series_list := cu.get_series_list()) == 0:
        print("No urls found.")
        print(f"The file {Config.CONFIG_DIR}/urls should contain a list of Wikpedia urls for TV series, one per line.")
        sys.exit(1)

    schedule.every().day.do(uh.check_new_seasons, series_list, cache_dir)

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


if __name__ == "__main__":
    main()
