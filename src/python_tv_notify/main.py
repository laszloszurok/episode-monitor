#!/usr/bin/env python

import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path

wiki_pages = [
    "https://en.wikipedia.org/wiki/Severance_(TV_series)",
    "https://en.wikipedia.org/wiki/What_We_Do_in_the_Shadows_(TV_series)",
]

for url in wiki_pages:

    req_str: str = requests.get(url=url).text
    html = BeautifulSoup(req_str, "html.parser")
    info_table = html.find(name="table", attrs={"class": "infobox vevent"})
    table_rows = info_table.contents[0].contents

    for tr in table_rows:
        if tr.text.startswith("No. of seasons"):

            cache_dir = (f"{xdg_cache}/tvnotipy" if (xdg_cache := os.getenv("XDG_CACHE_HOME"))
                          and os.path.isabs(xdg_cache) else Path.home().joinpath(".cache", "tvnotipy"))
            title = url.split("/")[-1]
            cache_file = os.path.join(cache_dir, title)

            if not os.path.isdir(cache_dir):
                os.makedirs(cache_dir)

            num_of_seasons_last = 0
            if os.path.isfile(cache_file):
                with open(cache_file) as file:
                    num_of_seasons_last = file.read()

            num_of_seasons_current=tr.text.replace("No. of seasons", "")

            if int(num_of_seasons_current) > int(num_of_seasons_last):
                print(f"new season for {title}")
                with open(cache_file, "w") as file:
                    file.writelines(num_of_seasons_current)
