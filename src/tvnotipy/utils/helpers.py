import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def check_new_seasons(series_list: list, cache_dir: Path):
    for series in series_list:
        req_str: str = requests.get(url=series["url"]).text
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
