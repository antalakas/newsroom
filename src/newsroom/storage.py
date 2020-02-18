# src/newsroom/storage.py
import datetime

import numpy as np
import tiledb
import tiledb.cloud


def get_timestamp_from_text(datetime_text):
    date_time_obj = datetime.datetime.strptime(datetime_text, "%Y-%m-%d %H:%M:%S")
    return int(datetime.datetime.timestamp(date_time_obj))


def get_datetime_from_timestamp(timestamp):
    timestamp = datetime.datetime.fromtimestamp(int(timestamp))
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def create_array(
    array_name, dim_medium, first_timestamp, last_timestamp, dim_article, tile_extent
):
    # The array will be 10000 x seconds_in_year x 100 with
    # dimensions "medium", "time", "article"

    print(int(dim_medium - tile_extent))
    print(first_timestamp)
    print(last_timestamp)
    print(int(dim_article - tile_extent))

    dom = tiledb.Domain(
        tiledb.Dim(
            name="medium",
            domain=(1, int(dim_medium - tile_extent)),
            tile=tile_extent,
            dtype=np.uint64,
        ),
        tiledb.Dim(
            name="time",
            domain=(first_timestamp, last_timestamp),
            tile=tile_extent,
            dtype=np.uint64,
        ),
        tiledb.Dim(
            name="article",
            domain=(1, int(dim_article - tile_extent)),
            tile=tile_extent,
            dtype=np.uint64,
        ),
    )

    # The array will be sparse, having following attributes
    schema = tiledb.ArraySchema(
        domain=dom,
        sparse=True,
        attrs=[
            tiledb.Attr(name="title", var=True, dtype="U"),
            tiledb.Attr(name="modyfication_date", dtype=np.uint64),
            tiledb.Attr(name="medium_text", dtype=np.dtype("U1")),
            tiledb.Attr(name="medium_group", dtype=np.dtype("U1")),
            tiledb.Attr(name="medium_pageviews", dtype=np.uint64),
            tiledb.Attr(name="is_blog", dtype=np.int8),
            tiledb.Attr(name="url", dtype=np.dtype("U1")),
            tiledb.Attr(name="advertising_value_equivalency", dtype=np.uint32),
            tiledb.Attr(name="keyword", dtype=np.dtype("U1")),
            tiledb.Attr(name="snippet", dtype=np.dtype("U1")),
            tiledb.Attr(name="text", dtype=np.dtype("U1")),
            tiledb.Attr(name="importance", dtype=np.float32),
            tiledb.Attr(name="sentiment", dtype=np.float32),
        ],
    )

    # Create the (empty) array on disk.
    tiledb.SparseArray.create(array_name, schema)


def read_array_s3(rest_adress, array_uri, token):
    config = tiledb.Config()
    config["rest.token"] = token
    config["rest.server_address"] = rest_adress
    config["vfs.s3.region"] = "eu-central-1"

    ctx = tiledb.Ctx(config)
    with tiledb.SparseArray(array_uri, ctx=ctx) as A:
        print(A[:]["title"])


def read_array_cloud_local(rest_address, array_uri, token):
    tiledb.cloud.login(host=rest_address, token=token)

    from_time = int(get_timestamp_from_text("2020-02-17 00:00:00"))
    print(from_time)
    to_time = int(get_timestamp_from_text("2020-02-17 23:59:59"))
    print(to_time)

    with tiledb.SparseArray(array_uri, ctx=tiledb.cloud.Ctx()) as A:
        # res = np.mean(A[:]["importance"])
        # print(res)

        # Returns all articles, if extreme bounds are added to regions,
        # there are less results
        res = A[:, from_time:to_time, :]
        # res = A[1:5000, from_time:to_time, 400000000:500000000]
        # <- for 2020-02-17 there are 217 results instead of 268

        # Returns all articles, need +1 because upper bound of the slice is not
        # inclusive
        # res = A[:, :, 443392586:443557994+1]

        article_dict = {}
        for i in range(len(res["title"])):
            article_dict[res["coords"][i][2]] = (
                get_datetime_from_timestamp(res["coords"][i][1]),
                res["medium_text"][i],
                res["title"][i],
            )

        for i in sorted(article_dict.keys()):
            print("%s: %s" % (i, article_dict[i]))

        print(len(res["title"]))


def read_array_sql(rest_address, array_uri, token):
    tiledb.cloud.login(host=rest_address, token=token)

    from_time = int(get_timestamp_from_text("2020-02-17 00:00:00"))
    print(from_time)
    to_time = int(get_timestamp_from_text("2020-02-17 23:59:59"))
    print(to_time)

    query = (
        "select min(article), max(article), count(article) from `"
        + array_uri
        + "` where `timestamp` BETWEEN "
        + str(from_time)
        + " and "
        + str(to_time)
    )
    print(query)

    res = tiledb.cloud.sql.exec(query=query)

    print(res)


def mean(numpy_ordered_dictionary):
    return np.mean(numpy_ordered_dictionary["importance"])
    # return numpy_ordered_dictionary


def read_array_cloud(rest_address, array_uri, token):
    tiledb.cloud.login(host=rest_address, token=token)

    from_time = int(get_timestamp_from_text("2020-02-04 00:00:00"))
    print(from_time)
    to_time = int(get_timestamp_from_text("2020-02-04 23:59:59"))
    print(to_time)

    with tiledb.SparseArray(array_uri, ctx=tiledb.cloud.Ctx()) as A:
        res = A.apply(
            mean,
            [(1, 5000), (from_time, to_time), (400000000, 500000000)],
            attrs=["importance"],
        )
        print(res)
