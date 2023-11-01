import os
from datetime import datetime
from pathlib import Path

import dbus
import requests
from bs4 import BeautifulSoup
from tvnotipy import timezone
from tvnotipy.config.constants import Condition


def check_new_seasons(series_list: list, cache_dir: Path):
    for series in series_list:
        req_str: str = requests.get(url=series["url"], timeout=10).text
        html = BeautifulSoup(req_str, "html.parser")
        info_table = html.find(name="table", attrs={"class": "infobox vevent"})
        table_rows = info_table.contents[0].contents

        for tr in table_rows:
            if tr.text.startswith("No. of seasons"):
                cache_file = os.path.join(cache_dir, series["cache_file"])

                num_of_seasons_last = 0
                if os.path.isfile(cache_file):
                    with open(cache_file) as file:
                        num_of_seasons_last = file.read()

                num_of_seasons_current = tr.text.replace("No. of seasons", "")

                if int(num_of_seasons_current) > int(num_of_seasons_last):
                    with open(cache_file, "w") as file:
                        file.writelines(num_of_seasons_current)


def is_modified_lately(file) -> bool:
    """Return true if the argument file was modified less than MAX_NOTIFY_AGE_DAYS days ago."""
    return (datetime.now(tz=timezone).timestamp() - os.path.getmtime(file)) / 86400 < Condition.MAX_NOTIFY_AGE_DAYS


def send_desktop_notification(title: str, message: str):
    obj = dbus.SessionBus().get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
    interface = dbus.Interface(obj, "org.freedesktop.Notifications")
    interface.Notify("", 0, "", f"{title}", f"{message}", [], {"urgency": 1}, 10000)
