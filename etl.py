import argparse
import pandas as pd
import psycopg2
import textwrap
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Insert data present in file at filepath as record into songs and artists
    tables.

    Args:
        cur cursor to Postgres db
        filepath absolute path to a file in data/song_data
    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.loc[0, ["song_id", "title", "artist_id", "year", "duration"]
                       ].apply(str).values.tolist()
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df.loc[0, ["artist_id", "artist_name", "artist_location",
                             "artist_latitude", "artist_longitude"]
                         ].values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Insert data present in file at filepath as record into songplays, users
    and time tables.

    Args:
        cur cursor to Postgres db
        filepath absolute path to a file in data/log_data
    Returns:
        None
    """
    pass


def process_data(cur, conn, filepath, func):
    """
    Process all files in filepath using func.

    Args:
        cur cursor to Postgres db
        conn connection to Postgres db
        filepath "data/log_data" or "data/song_data"
        func process_log_file or process_song_file respectively
    Returns:
        None
    """
    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("\
            Load song play logs and song metadata to Postgres. The script \n\
            assumes that logs are stored under ./data/log_data and song \n\
            metadata under ./data/song_data")
    )

    # obtain postgres connection parameters
    for arg in ["host", "dbname", "user", "password"]:
        parser.add_argument("--" + arg, required=True)
    args = parser.parse_args()

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={}".format(
            args.host,
            args.dbname,
            args.user,
            args.password
        )
    )
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()
