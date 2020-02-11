# src/newsroom/storage.py
import numpy as np
import tiledb


def create_array(array_name, dim_medium, first_timestamp, last_timestamp, dim_article):
    # The array will be 10000 x seconds_in_year x 100 with
    # dimensions "medium", "time", "article"
    dom = tiledb.Domain(
        tiledb.Dim(
            name="medium", domain=(1, int(dim_medium)), tile=100, dtype=np.uint64
        ),
        tiledb.Dim(
            name="time",
            domain=(first_timestamp, last_timestamp),
            tile=1000,
            dtype=np.uint64,
        ),
        tiledb.Dim(
            name="article", domain=(1, int(dim_article)), tile=5, dtype=np.uint64
        ),
    )

    # The array will be sparse, having following attributes
    schema = tiledb.ArraySchema(
        domain=dom, sparse=True, attrs=[tiledb.Attr(name="a", dtype=np.int32)]
    )

    # Create the (empty) array on disk.
    tiledb.SparseArray.create(array_name, schema)
