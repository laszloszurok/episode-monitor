#!/usr/bin/env python

import os
import sys
import time
from datetime import datetime
from pathlib import Path

import dbus
import requests
import schedule
from bs4 import BeautifulSoup

cache_dir = (
    f"{xdg_cache}/tvnotipy"
    if (xdg_cache := os.getenv("XDG_CACHE_HOME")) and os.path.isabs(xdg_cache)
    else Path.home().joinpath(".cache", "tvnotipy")
)

config_dir = (
    f"{xdg_config}/tvnotipy"
    if (xdg_config := os.getenv("XDG_CONFIG_HOME")) and os.path.isabs(xdg_config)
    else Path.home().joinpath(".config", "tvnotipy")
)

urls_file = os.path.join(config_dir, "urls")

if os.path.isfile(urls_file):
    with open(urls_file) as file:
        urls = [line.strip() for line in file]
    if len(urls) == 0:
        print(f"{urls_file} is empty. The file should contain a list of Wikipedia urls of TV series, one per line.")
        sys.exit(1)
else:
    print(f"{urls_file} is empty. The file should contain a list of Wikipedia urls of TV series, one per line.")
    sys.exit(1)


def job():
    for url in urls:
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

    for url in urls:
        title = url.split("/")[-1]
        cache_file = os.path.join(cache_dir, title)
        if os.path.isfile(cache_file):
            if ((datetime.now().timestamp() - os.path.getmtime(cache_file)) / (60 * 60 * 24)) < 2:
                obj = dbus.SessionBus().get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
                interface = dbus.Interface(obj, "org.freedesktop.Notifications")
                interface.Notify("", 0, "", "New season", f"{title}", [], {"urgency": 1}, 10000)

    time.sleep(7200)
