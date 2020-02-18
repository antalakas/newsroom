# src/newsroom/read_array.py
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
    "--read_type",
    "-wt",
    default="cloud_local",
    help="Type of read operation",
    metavar="WRITETYPE",
    show_default=True,
)
@click.version_option(version=__version__)
def main(year, read_type):
    """
    Reads from TileDB array
    """
    # Name of array
    # array_name = "newsroom_" + year

    # Rest address
    # production
    rest_adress = "https://api.tiledb.com/v1"
    # master /staging
    # rest_adress = "https://master.tiledb-rest-prototype.dev.tiledb.io/v1"

    # URI of S3 array
    array_s3_uri = "s3://eu-frankfurt-01/newsroom_2020"

    # URI of TileDB array
    array_tiledb_uri = "tiledb://andreas/newsroom_2020"

    # Service token
    token = "Please replace with your token"

    if read_type == "s3":
        storage.read_array_s3(rest_adress, array_s3_uri, token)

    if read_type == "cloud_local":
        storage.read_array_cloud_local(rest_adress, array_tiledb_uri, token)

    if read_type == "sql":
        storage.read_array_sql(rest_adress, array_tiledb_uri, token)

    # Not working with poetry
    if read_type == "cloud":
        storage.read_array_cloud(rest_adress, array_tiledb_uri, token)
