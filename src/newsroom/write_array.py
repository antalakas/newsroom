# src/newsroom/write_array.py
import click

from . import __version__

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
    "--write_type",
    "-wt",
    default="once",
    help="Type of write operation",
    metavar="WRITETYPE",
    show_default=True,
)
@click.version_option(version=__version__)
def main(year, write_type):
    """
    Writes to TileDB array
    """
    # Name of array
    # array_name = "newsroom_" + year

    # !!! WRITING FROM PYTHON IS DISABLED !!!

    # if write_type == "once":
    #     # Write to array
    #     storage.write_array_once(array_name)

    # if write_type == "multi":
    #     # Write to array
    #     storage.write_array_multi(array_name)
