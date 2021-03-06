# src/newsroom/create_array.py
import sys

import click

from . import __version__, storage

# Regarding maxint
# https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints


@click.command()
@click.option(
    "--year",
    "-y",
    default="2020",
    help="Year of the file, expressed in seconds for dimension dim_time",
    metavar="YEAR",
    show_default=True,
)
@click.option(
    "--dim_medium",
    "-dm",
    default=sys.maxsize * 2 + 1,
    help="Medium Id",
    metavar="DIMMEDIUM",
    show_default=True,
)
@click.option(
    "--dim_article",
    "-da",
    default=sys.maxsize * 2 + 1,
    help="Articles from a specific medium at the same second in year",
    metavar="DIMARTICLE",
    show_default=True,
)
@click.option(
    "--tile_extent",
    "-te",
    default=1000,
    help="Tile Extent for TileDB array",
    metavar="TILEEXTENT",
    show_default=True,
)
@click.version_option(version=__version__)
def main(year, dim_medium, dim_article, tile_extent):
    """
    Generates a TileDB array to host news
    """
    first_day = year + "-01-01 00:00:00"
    last_day = year + "-12-31 23:59:59"

    # Calculate timestamps for dim_time dimension limits
    first_timestamp = storage.get_timestamp_from_text(first_day)
    last_timestamp = storage.get_timestamp_from_text(last_day)

    # Name of array
    array_name = "newsroom_" + year

    # Create the array
    storage.create_array(
        array_name,
        dim_medium,
        first_timestamp,
        last_timestamp,
        dim_article,
        tile_extent,
    )
