import os

from config.constants import Config


def get_cache_dir():
    if not os.path.isdir(Config.CACHE_DIR):
        os.makedirs(Config.CACHE_DIR)
    return Config.CACHE_DIR


def get_urls_list() -> list:
    urls = []

    if os.path.isfile(Config.URLS_FILE):
        with open(Config.URLS_FILE) as file:
            urls = [line.strip() for line in file]

    return urls


def get_series_list() -> list:
    """Returns a list of obects in {"url": url, "cache_file": filepath} format,
    where 'url' is the wiki page url from the config file and 'filepath' is
    extracted from the url itself.

    Usage:
      myvar = get_series_list()
      print(myvar['url'], myvar['cache_file'])
    """
    return [{"url": url, "cache_file": os.path.join(Config.CACHE_DIR, url.split("/")[-1])} for url in get_urls_list()]
