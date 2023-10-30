#!/usr/bin/env python

import os
import time
from datetime import datetime

import config.utils as cu
import dbus
import requests
import schedule
from bs4 import BeautifulSoup

cache_dir = cu.get_cache_dir()
series_list = cu.get_series_list()


def check_new_seasons():
    for series in series_list:
        req_str: str = requests.get(url=series["url"]).text
        html = BeautifulSoup(req_str, "html.parser")
        info_table = html.find(name="table", attrs={"class": "infobox vevent"})
        table_rows = info_table.contents[0].contents

        for tr in table_rows:
            if tr.text.startswith("No. of seasons"):
                cache_file = os.path.join(cache_dir, series["cache_file_name"])

                num_of_seasons_last = 0
                if os.path.isfile(cache_file):
                    with open(cache_file) as file:
                        num_of_seasons_last = file.read()

                num_of_seasons_current = tr.text.replace("No. of seasons", "")

                if int(num_of_seasons_current) > int(num_of_seasons_last):
                    with open(cache_file, "w") as file:
                        file.writelines(num_of_seasons_current)


schedule.every().day.do(check_new_seasons)

while True:
    schedule.run_pending()

    for series in series_list:
        cache_file = series["cache_file"]
        if os.path.isfile(cache_file):
            if ((datetime.now().timestamp() - os.path.getmtime(cache_file)) / (60 * 60 * 24)) < 2:
                title = str(cache_file).split("/")[-1]
                obj = dbus.SessionBus().get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
                interface = dbus.Interface(obj, "org.freedesktop.Notifications")
                interface.Notify("", 0, "", "New season", f"{title}", [], {"urgency": 1}, 10000)

    time.sleep(7200)
