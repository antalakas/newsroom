# src/newsroom/ingest_news.py
from os import listdir
from os.path import isfile, join

import click

from . import __version__, news_file


@click.command()
@click.version_option(version=__version__)
def main():
    """Newsroom Python project."""
    news_path = "/Users/andreas/workspace/newsroom/news"
    news_files = [f for f in listdir(news_path) if isfile(join(news_path, f))]

    # print(onlyfiles)

    min = 1000000
    max = 0
    dict = {}

    for f in news_files:
        file_name = join(news_path, f)
        print(file_name)
        min, max, dict = news_file.read_file(file_name, min, max, dict)
        # break

    print(min)
    print(max)

    for key in sorted(dict):
        print("%s: %s" % (key, dict[key]))

    print(len(dict))
