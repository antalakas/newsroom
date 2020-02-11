# src/newsroom/create_array.py
import datetime

import click

from . import __version__, storage


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
    default="10000",
    help="Medium Id",
    metavar="DIMMEDIUM",
    show_default=True,
)
@click.option(
    "--dim_article",
    "-da",
    default="100",
    help="Articles from a specific medium at the same second in year",
    metavar="DIMARTICLE",
    show_default=True,
)
@click.version_option(version=__version__)
def main(year, dim_medium, dim_article):
    """
    Generates a TileDB array to host news
    """
    first_day = year + "-01-01"
    last_day = year + "-12-31"

    # Create date objects in given time format yyyy-mm-dd
    first_date = datetime.datetime.strptime(first_day, "%Y-%m-%d")
    last_date = datetime.datetime.strptime(last_day, "%Y-%m-%d")

    # Calculate timestamps for dim_time dimension limits
    first_timestamp = int(datetime.datetime.timestamp(first_date))
    last_timestamp = int(datetime.datetime.timestamp(last_date))

    # Name of array
    array_name = "newsroom_" + year

    # Create the array
    storage.create_array(
        array_name, dim_medium, first_timestamp, last_timestamp, dim_article
    )