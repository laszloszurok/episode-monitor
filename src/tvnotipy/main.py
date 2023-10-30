#!/usr/bin/env python

import os
import time
from datetime import datetime
from pathlib import Path

import dbus
import requests
import schedule
from bs4 import BeautifulSoup

wiki_pages = [
    "https://en.wikipedia.org/wiki/Severance_(TV_series)",
    "https://en.wikipedia.org/wiki/What_We_Do_in_the_Shadows_(TV_series)",
    "https://en.wikipedia.org/wiki/Stranger_Things",
]

cache_dir = (
    f"{xdg_cache}/tvnotipy"
    if (xdg_cache := os.getenv("XDG_CACHE_HOME")) and os.path.isabs(xdg_cache)
    else Path.home().joinpath(".cache", "tvnotipy")
)

def job():
    for url in wiki_pages:
        req_str: str = requests.get(url=url).text
        html = BeautifulSoup(req_str, "html.parser")
        info_table = html.find(name="table", attrs={"class": "infobox vevent"})
        table_rows = info_table.contents[0].contents

        for tr in table_rows:
            if tr.text.startswith("No. of seasons"):
                title = url.split("/")[-1]
                cache_file = os.path.join(cache_dir, title)

                if not os.path.isdir(cache_dir):
                    os.makedirs(cache_dir)

                num_of_seasons_last = 0
                if os.path.isfile(cache_file):
                    with open(cache_file) as file:
                        num_of_seasons_last = file.read()

                num_of_seasons_current = tr.text.replace("No. of seasons", "")

                if int(num_of_seasons_current) > int(num_of_seasons_last):
                    with open(cache_file, "w") as file:
                        file.writelines(num_of_seasons_current)


schedule.every().day.do(job)

while True:
    schedule.run_pending()

    for url in wiki_pages:
        title = url.split("/")[-1]
        cache_file = os.path.join(cache_dir, title)
        if os.path.isfile(cache_file):
            if ((datetime.now().timestamp() - os.path.getmtime(cache_file)) / (60 * 60 * 24)) < 2:
                obj = dbus.SessionBus().get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
                interface = dbus.Interface(obj, "org.freedesktop.Notifications")
                interface.Notify("", 0, "", "New season", f"{title}", [], {"urgency": 1}, 10000)

    time.sleep(7200)
