# src/newsroom/medium_map_generator.py
import json
from os import listdir
from os.path import isfile, join

import click

from . import __version__, news_file


@click.command()
@click.option(
    "--medium_map_version",
    "-mmv",
    default="1",
    help="Verion of map from MediumId to DimensionId",
    metavar="MAPVER",
    show_default=True,
)
@click.version_option(version=__version__)
def main(medium_map_version):
    """
    Generates and saves to disk a map from mediumId to DimensionId.
    The map should have a version, of the same datatype as DimensionId.
    Version can be stored at map[0] element
    Key: uint32, Datatype: uint32
    """
    base_path = "/Users/andreas/workspace/newsroom"

    news_path = base_path + "/news"

    medium_map_name = "medium_map"
    medium_map_path = base_path + "/" + medium_map_name + "/" + str(medium_map_version)

    news_files = [f for f in listdir(news_path) if isfile(join(news_path, f))]

    medium_dict = {}
    dim_id = 0
    num_of_items = 0
    medium_dict[dim_id] = medium_map_version
    stats_dict = {}

    for f in news_files:
        file_name = join(news_path, f)
        dim_id, num_of_items, medium_dict, stats_dict = news_file.get_file_stats(
            file_name, dim_id, num_of_items, medium_dict, stats_dict
        )

    for key in sorted(stats_dict):
        print(
            "MediumId: %s, Num of items: %s, DimensionId: %s"
            % (key, stats_dict[key], medium_dict[key])
        )
    print("\nTotal num of medium Ids: %s" % (len(stats_dict)))
    print("\nTotal num of items: %s" % (num_of_items))

    save_medium_map(medium_dict, medium_map_path, medium_map_name)


def save_medium_map(obj, path, name):
    j = json.dumps(obj)
    f = open(path + "/" + name + ".json", "w")
    f.write(j)
    f.close()
